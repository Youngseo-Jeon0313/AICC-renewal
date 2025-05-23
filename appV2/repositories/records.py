from config.database import get_db_connection 

def get_record_from_db(task_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM records WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return task

def get_text_from_record(task_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT stt_result FROM records WHERE id = %s", (task_id,))
    text = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return text

def get_record_status(task_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT is_stt_completed FROM records WHERE id = %s", (task_id,))
    status = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return status

def update_record_status(task_id, stt_result):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE records SET stt_result = %s, is_stt_completed = 1 WHERE id = %s",
        (stt_result, task_id)
    )    
    conn.commit()
    success = cursor.rowcount > 0

    cursor.close()
    conn.close()
    
    return success
