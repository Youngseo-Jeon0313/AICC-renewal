from flask import Flask, request, jsonify
from celery_config import celery
from repositories.records import get_text_from_record, get_record_status, get_record_from_db
import redis
import json
from datetime import datetime

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6380, db=0) # Redis client에 worker의 상태 저장

@app.route('/record/stt', methods=['GET'])
def get_stt_from_record():
    record_id = request.args.get('record_id')
    if not record_id:
        return jsonify({'status': 'error', 'message': 'record_id는 필수입니다'}), 400

    record = get_record_from_db(record_id)
    if not record:
        return jsonify({'status': 'error', 'message': '녹음본을 찾을 수 없습니다'}), 404

    # 1. DB 확인
    is_stt_completed = get_record_status(record_id)
    if is_stt_completed.get('is_stt_completed') == 1:
        text = get_text_from_record(record_id)
        # DB에 저장되어 있다면, Redis 상태 정리
        clear_worker_status(record_id)
        return jsonify({
            'status': 'success',
            'message': text.get('stt_result') if text else '빈 텍스트입니다.' # 텍스트가 비어있음
        })

    # 2. Redis에서 작업 상태 확인
    worker_status = get_worker_status(record_id)
    if worker_status:
        status_data = json.loads(worker_status)
        if status_data.get('status') == 'processing':
            return jsonify({
                'status': 'processing',
                'message': 'STT 작업이 진행 중입니다. 잠시 후 다시 시도해 주세요.',
            }), 202
        elif status_data.get('status') == 'completed':
            # Redis에 임시 저장된 결과가 있다면 반환
            result = redis_client.get(f"stt_result:{record_id}")
            if result:
                return jsonify({
                    'status': 'success',
                    'message': json.loads(result),
                })

    # 3. 새로운 작업 시작
    try:
        celery.send_task('process_task', args=[record_id])
        set_worker_status(record_id, json.dumps({
            'status': 'processing',
            'started_at': datetime.now().isoformat()
        }))
        return jsonify({
            'status': 'success',
            'message': f'작업 {record_id}에 대한 STT를 진행합니다. 잠시만 기다려 주세요.',
            'record_id': record_id
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def get_worker_status(record_id):
    status_key = f"stt_status:{record_id}"
    return redis_client.get(status_key)

def set_worker_status(record_id, status):
    status_key = f"stt_status:{record_id}"
    redis_client.setex(status_key, 600, status)  # 10분 TTL 

def clear_worker_status(record_id):
    status_key = f"stt_status:{record_id}"
    result_key = f"stt_result:{record_id}"
    redis_client.delete(status_key, result_key)
