import random
import time

def get_position_in_queue(q, target_job):
    all_jobs = q.jobs
    # 현재 작업이 큐에서 몇 번째에 위치하는지 확인
    position = all_jobs.index(target_job) + 1 if target_job in all_jobs else None
    return position

def random_job(*args, **kargs):
    t = random.randint(1,20)
    time.sleep(t)
    return t

def on_success(job, connection, result, *args, **kargs):
    print(f"the job {job.latest_result().job_id} terminated successfully with result: {result}")

def on_failure(job, connection, type, value, traceback, *args, **kargs):
    print(f"the job {job.latest_result().job_id} terminated with errors: {traceback}")
