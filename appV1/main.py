from flask import Flask, jsonify, request
from redis import Redis
from flask_restx import Api, Resource, fields
from rq import Queue
import time
import os
from models.api_models import create_api_models

# Redis keys
QUEUE_KEY = "request_queue"  # List 자료구조 - 큐 역할
SET_KEY = "request_set"    # Set 자료구조 - 중복 체크용

app = Flask(__name__)
api = Api(app, version='1.0', title='STT 처리 시스템 API',
          description='Flask 기반의 STT 처리 시스템 API')

# swagger 네임스페이스
queue_ns = api.namespace('queue', description='큐 작업 관련 API')
text_ns = api.namespace('text', description='텍스트 생성 관련 API')

redis = Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

q = Queue(connection=redis)

# API 모델
api_models = create_api_models(api)

@queue_ns.route('/enqueue')
class EnqueueJob(Resource):
    @api.expect(api_models['job_model'])
    @api.response(200, '작업이 성공적으로 큐에 추가됨')
    @api.response(400, '잘못된 요청 또는 중복된 작업')
    def post(self):
        try:
            data = request.get_json()
            record_id = data.get('record_id')
            priority = int(time.time() * 1000)

            if not record_id:
                return {'status': 'error', 'message': 'record_id는 필수입니다'}, 400

            if redis.zscore(SET_KEY, record_id) is not None:
                return {'status': 'error', 'message': f'record_id {record_id}는 이미 큐에 존재합니다'}, 400

            pipe = redis.pipeline()
            pipe.zadd(SET_KEY, {record_id: priority})
            pipe.rpush(QUEUE_KEY, record_id)
            pipe.execute()

            queue_length = redis.llen(QUEUE_KEY)
            position = redis.lpos(QUEUE_KEY, record_id)

            return {
                'status': 'success',
                'message': f'작업 {record_id}가 큐에 추가되었습니다',
                'position': position + 1,
                'queue_length': queue_length
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)