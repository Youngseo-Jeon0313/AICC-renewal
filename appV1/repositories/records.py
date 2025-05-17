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