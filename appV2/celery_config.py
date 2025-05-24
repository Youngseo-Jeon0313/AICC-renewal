from celery import Celery
import os
import cpu1
import cpu2

# Celery 설정
broker_url = os.getenv('CELERY_BROKER_URL', 'redis://redis:6380/0')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6380/0')

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Seoul'
enable_utc = True

celery = Celery(
    'stt_tasks',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://redis:6380/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6380/0')
)
