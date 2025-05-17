from flask import Flask, jsonify, request
from redis import Redis
from flask_restx import Api, Resource
from rq import Queue
import time
import os
from models.api_models import create_api_models
from repositories.records import get_text_from_record, get_record_status

# Redis keys
QUEUE_KEY = "request_queue"  # List 자료구조 - 큐 역할
SET_KEY = "request_set"    # Set 자료구조 - 중복 체크용

app = Flask(__name__)
api = Api(app, version='1.0', title='STT 처리 시스템 API',
          description='Flask 기반의 STT 처리 시스템 API')

# swagger 네임스페이스
record_ns = api.namespace('record', description='record 관련 API')

redis = Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

q = Queue(connection=redis)

# API 모델
api_models = create_api_models(api)

@record_ns.route('/job')
class EnqueueJob(Resource):
    @api.expect(api_models['job_model'])
    @api.response(200, '작업이 성공적으로 요청됨')
    @api.response(400, '잘못된 요청 또는 중복된 작업')
    def post(self):
        try:
            data = request.get_json()
            record_id = data.get('record_id')
            if not record_id:
                return {'status': 'error', 'message': 'record_id는 필수입니다'}, 400
            
            priority = int(time.time() * 1000)

            is_stt_completed = get_record_status(record_id)
            if is_stt_completed == 1:
                return {'status': 'success', 'message': get_text_from_record(record_id)}
                
            if redis.zscore(SET_KEY, record_id) is not None:
                return {'status': 'error', 'message': f'record_id {record_id}는 이미 큐에 존재합니다'}, 400

            pipe = redis.pipeline()
            pipe.zadd(SET_KEY, {record_id: priority}) # key: record_id, value: priority(timestamp)
            pipe.rpush(QUEUE_KEY, record_id)
            pipe.execute()

            queue_length = redis.llen(QUEUE_KEY)
            position = redis.lpos(QUEUE_KEY, record_id)

            return {
                'status': 'success',
                'message': f'작업 {record_id}에 대한 STT를 진행합니다. 잠시만 기다려 주세요.',
                'position': position + 1,
                'queue_length': queue_length
            }
        
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500


# 폴링 형태로 DB에 있는 내 record_id의 상태를 확인하는 API
@record_ns.route('/job/<int:record_id>')
class JobStatus(Resource):
    @api.response(200, '작업 상태 조회 성공')
    @api.response(404, '작업을 찾을 수 없음')
    def get(self, record_id):
        try:
            text = get_text_from_record(record_id)
            if text:
                return {
                    'status': 'success',
                    'message': text,
                }
            else:
                return {'status': 'error', 'message': f'record_id {record_id}에 대한 작업이 없습니다'}, 404
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500
        
if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
