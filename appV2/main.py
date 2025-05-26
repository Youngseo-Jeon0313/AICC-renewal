from flask import Flask, request, jsonify
from celery_config import celery
from repositories.records import get_text_from_record, get_record_status, get_record_from_db
from celery.result import AsyncResult

app = Flask(__name__)

@app.route('/record/stt', methods=['GET'])
def get_stt_from_record():
    record_id = request.args.get('record_id')
    if not record_id:
        return jsonify({'status': 'error', 'message': 'record_id는 필수입니다'}), 400

    record = get_record_from_db(record_id)
    if not record:
        return jsonify({'status': 'error', 'message': '녹음본을 찾을 수 없습니다'}), 404

    is_stt_completed = get_record_status(record_id)
    if is_stt_completed.get('is_stt_completed') == 1:
        text = get_text_from_record(record_id)
        return jsonify({
            'status': 'success',
            'message': text.get('stt_result') if text else '빈 텍스트입니다.' # 텍스트가 비어있음
        })

    # DB에 아직 stt 안되어있음
    try:
        task_result = AsyncResult(record_id, app=celery) # Celery 작업 상태 확인
        # 큐에 작업이 있음
        if task_result.ready():
            result = task_result.get() # 실제 작업 결과 꺼냄
            if result.get('status') == 'completed':
                text = get_text_from_record(result['record_id'])
                if text:
                    return jsonify({
                        'status': 'success',
                        'message': text.get('stt_result'),
                        'processor': result.get('processor', 'Unknown')
                    })
                else:
                    return jsonify({
                        'status': 'error',
                        'message': '빈 텍스트입니다.'
                    }), 404
            else:
                return jsonify({'status': 'processing', 'message': 'STT 작업이 진행 중입니다. 잠시 후 다시 시도해 주세요.'}), 202
        # 큐에 작업이 없음
        else:
            # 작업이 없으면 새로 큐에 넣음
            celery.send_task('process_task', args=[record_id])
            return jsonify({
                'status': 'success',
                'message': f'작업 {record_id}에 대한 STT를 진행합니다. 잠시만 기다려 주세요.',
                'record_id': record_id
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
