import redis
import time
import json
from config.database import get_db_connection
from repositories.records import get_record_from_db
import os
from services.text_generator import TextGenerator

# Redis 연결 설정
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

SET_KEY = "request_set"

def process_task(record_id: int):
    task_data = get_record_from_db(record_id)
    # record_duration을 초 단위의 정수로 변환
    duration_seconds = int((task_data['record_end_time'] - task_data['record_start_time']).total_seconds())
    generate_text_result = TextGenerator.generate_text(duration_seconds)
    
    return {
        'task_id': task_data['id'],
        'record_duration': duration_seconds,
        'stt_result': generate_text_result.text,
        'processor': 'CPU2'
    }

def save_result(result):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE records 
            SET stt_result = %s,
                is_stt_completed = TRUE
            WHERE id = %s
        """
        cursor.execute(sql, (
            result['stt_result'],
            result['task_id']
        ))
        conn.commit()
    except Exception as e:
        print(f"Error saving to database: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    print("CPU2 worker started")
    while True:
        try:
            task = redis_client.zpopmin('request_set', count=1)

            if task:
                record_id = int(task[0][0])
                print(f"CPU2 processing task: {record_id}")

                result = process_task(record_id)
                save_result(result)
                print(f"CPU2 completed task: {record_id}")

                # 바로 다음 작업 시도
                time.sleep(0.1)
            else:
                print("No task found. Sleeping for 10 seconds.")
                time.sleep(10)

        except Exception as e:
            print(f"Error in CPU2 worker: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
