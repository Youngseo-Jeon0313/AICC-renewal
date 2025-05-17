CREATE TABLE IF NOT EXISTS records (
     id INT AUTO_INCREMENT PRIMARY KEY,
     recording_url TEXT,
     stt_result TEXT,
     is_stt_completed BOOLEAN DEFAULT FALSE,
     record_start_time DATETIME,
     record_end_time DATETIME,
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
