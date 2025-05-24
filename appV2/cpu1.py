from celery import shared_task
from repositories.records import get_record_from_db, update_record_status
from services.text_generator import TextGenerator
from time import sleep

@shared_task(name='process_task', queue='cpu1')
def process_task(record_id: int):
    """CPU1에서 STT 처리를 수행하는 Celery Worker"""
    try:
        task_data = get_record_from_db(record_id)
        if not task_data:
            return {'status': 'error', 'record_id': record_id, 'error': 'Record not found'}
        
        # record_duration을 초 단위의 정수로 변환
        duration_seconds = int((task_data['record_end_time'] - task_data['record_start_time']).total_seconds())
        sleep(duration_seconds) # duration_seconds만큼 wait
        generate_text_result = TextGenerator.generate_text(duration_seconds)
        
        result = {
            'task_id': task_data['id'],
            'record_duration': duration_seconds,
            'stt_result': generate_text_result.text,
            'processor': 'CPU1'
        }
        
        update_success = update_record_status(result['task_id'], result['stt_result'])
        
        if update_success:
            return {'status': 'completed', 'record_id': record_id, 'text': result['stt_result']}
        else:
            return {'status': 'error', 'record_id': record_id, 'error': 'Failed to update database'}
            
    except Exception as e:
        return {'status': 'error', 'record_id': record_id, 'error': str(e)}
