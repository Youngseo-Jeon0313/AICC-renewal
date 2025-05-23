from celery import Celery
import os

# Celery 설정
broker_url = os.getenv('CELERY_BROKER_URL', 'redis://redis:6380/0')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6380/0')

# 작업 큐 설정
task_queues = {
    'stt_queue': {
        'exchange': 'stt',
        'routing_key': 'stt.process',
    }
}

# 작업 라우팅 설정
task_routes = {
    'tasks.process_stt': {'queue': 'stt_queue'},
}

# 작업 시리얼라이저 설정
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Seoul'
enable_utc = True

celery = Celery(
    __name__,
    broker=broker_url,
    backend=result_backend,
)

@celery.task
def divide(x, y): # test
    import time
    time.sleep(5)
    return x / y