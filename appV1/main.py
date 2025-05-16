from flask import Flask, jsonify, request
from redis import Redis
from rq import Queue
import time
from services.tasks import random_job

# Sorted Set의 키
QUEUE_KEY = "request"

app = Flask(__name__)
redis = Redis(host='redis', port=6379, db=0)

q = Queue(connection=redis)

@app.route('/job_result/<job_id>', methods=['GET'])
def poll_result(job_id):
    job = q.fetch_job(job_id)

    if job is not None:
        if job.is_finished:
            result = job.result

            # 작업이 완료되면 Redis에 결과 저장하고 q에서 job 삭제
            redis.set(f'result:{job_id}', result)
            job.cleanup()

            return jsonify({'status': 'success', 'message': 'Job finished', 'result': result})
        elif job.is_failed:
            job.cleanup()
            return jsonify({'status': 'error', 'message': 'Job failed'})
        elif job.is_started:
            # 현재 작업 중
            return jsonify({'status': 'success', 'message': f'Job still in progress, position in queue: 0'})
        elif job.is_queued:
            # 큐에서 현재 작업 위치
            queued_jobs = q.job_ids
            position = queued_jobs.index(job_id) + 1

            return jsonify({'status': 'success', 'message': f'Job queued, position in queue: {position}/{len(queued_jobs)}'})
    else:
        return jsonify({'status': 'error', 'message': 'Job not found'})


@app.route('/enqueue', methods=['POST'])
def enqueue_job():
    data = request.get_json()
    job_id = data.get('job_id')

    if job_id:
        q.enqueue(random_job, job_id=job_id)
        return jsonify({'status': 'success', 'message': f'Job {job_id} enqueued'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid data'})

@app.route('/poll/<int:client_id>')
def poll(client_id):
    timeout = 60

    start_time = time.time()
    while time.time() - start_time < timeout:
        next_request = redis.zrange(QUEUE_KEY, 0, 0, withscores=True)
        if next_request:
            request, score = next_request[0]
            # 처리된 요청은 큐에서 제거
            redis.zrem(QUEUE_KEY, request)
            return jsonify({"status": "success", "client_id": client_id, "processed_request": request, "priority": score})
        time.sleep(1)

    return jsonify({"status": "timeout", "client_id": client_id})

@app.route('/get_requests', methods=['GET'])
def get_requests():
    all_jobs = q.jobs
    job_list = [{'job_id': job.id, 'status': job.get_status()} for job in all_jobs]
    return jsonify(job_list)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)