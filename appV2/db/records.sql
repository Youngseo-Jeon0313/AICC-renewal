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


INSERT INTO records (recording_url, stt_result, is_stt_completed, record_start_time, record_end_time, created_at, updated_at)
VALUES
    ('https://example.com/audio1.mp3', 'Hello, this is a test recording.', TRUE, '2025-05-17 09:00:00', '2025-05-17 09:01:00', NOW(), NOW()),
    ('https://example.com/audio2.mp3', 'The quick brown fox jumps over the lazy dog.', TRUE, '2025-05-17 09:02:00', '2025-05-17 09:03:30', NOW(), NOW()),
    ('https://example.com/audio3.mp3', NULL, FALSE, '2025-05-17 09:04:00', '2025-05-17 09:05:00', NOW(), NOW()),
    ('https://example.com/audio4.mp3', 'Speech-to-text in progress.', FALSE, '2025-05-17 09:06:00', '2025-05-17 09:07:00', NOW(), NOW()),
    ('https://example.com/audio5.mp3', 'Meeting summary recorded.', TRUE, '2025-05-17 09:08:00', '2025-05-17 09:10:00', NOW(), NOW()),
    ('https://example.com/audio6.mp3', NULL, FALSE, '2025-05-17 09:11:00', '2025-05-17 09:11:50', NOW(), NOW()),
    ('https://example.com/audio7.mp3', 'Agenda item number three.', TRUE, '2025-05-17 09:12:00', '2025-05-17 09:13:10', NOW(), NOW()),
    ('https://example.com/audio8.mp3', 'Record test one two three.', TRUE, '2025-05-17 09:14:00', '2025-05-17 09:15:00', NOW(), NOW()),
    ('https://example.com/audio9.mp3', NULL, FALSE, '2025-05-17 09:16:00', '2025-05-17 09:17:30', NOW(), NOW()),
    ('https://example.com/audio10.mp3', 'Customer support call.', TRUE, '2025-05-17 09:18:00', '2025-05-17 09:19:20', NOW(), NOW()),
    ('https://example.com/audio11.mp3', NULL, FALSE, '2025-05-17 09:20:00', '2025-05-17 09:21:00', NOW(), NOW()),
    ('https://example.com/audio12.mp3', 'Weather forecast update.', TRUE, '2025-05-17 09:22:00', '2025-05-17 09:23:15', NOW(), NOW()),
    ('https://example.com/audio13.mp3', 'Interview question number five.', TRUE, '2025-05-17 09:24:00', '2025-05-17 09:25:00', NOW(), NOW()),
    ('https://example.com/audio14.mp3', NULL, FALSE, '2025-05-17 09:26:00', '2025-05-17 09:27:00', NOW(), NOW()),
    ('https://example.com/audio15.mp3', 'Zoom call recording.', TRUE, '2025-05-17 09:28:00', '2025-05-17 09:29:00', NOW(), NOW()),
    ('https://example.com/audio16.mp3', NULL, FALSE, '2025-05-17 09:30:00', '2025-05-17 09:31:00', NOW(), NOW()),
    ('https://example.com/audio17.mp3', 'Project kickoff meeting.', TRUE, '2025-05-17 09:32:00', '2025-05-17 09:33:40', NOW(), NOW()),
    ('https://example.com/audio18.mp3', 'Audio test for microphone.', TRUE, '2025-05-17 09:34:00', '2025-05-17 09:34:50', NOW(), NOW()),
    ('https://example.com/audio19.mp3', NULL, FALSE, '2025-05-17 09:35:00', '2025-05-17 09:36:00', NOW(), NOW()),
    ('https://example.com/audio20.mp3', 'Marketing team call.', TRUE, '2025-05-17 09:37:00', '2025-05-17 09:38:20', NOW(), NOW()),
    ('https://example.com/audio21.mp3', NULL, FALSE, '2025-05-17 09:39:00', '2025-05-17 09:40:10', NOW(), NOW()),
    ('https://example.com/audio22.mp3', 'Technical support hotline.', TRUE, '2025-05-17 09:41:00', '2025-05-17 09:42:00', NOW(), NOW()),
    ('https://example.com/audio23.mp3', NULL, FALSE, '2025-05-17 09:43:00', '2025-05-17 09:44:00', NOW(), NOW()),
    ('https://example.com/audio24.mp3', 'Training session intro.', TRUE, '2025-05-17 09:45:00', '2025-05-17 09:46:30', NOW(), NOW()),
    ('https://example.com/audio25.mp3', NULL, FALSE, '2025-05-17 09:47:00', '2025-05-17 09:48:00', NOW(), NOW()),
    ('https://example.com/audio26.mp3', 'Daily scrum standup.', TRUE, '2025-05-17 09:49:00', '2025-05-17 09:50:10', NOW(), NOW()),
    ('https://example.com/audio27.mp3', NULL, FALSE, '2025-05-17 09:51:00', '2025-05-17 09:52:00', NOW(), NOW()),
    ('https://example.com/audio28.mp3', 'Online class lecture.', TRUE, '2025-05-17 09:53:00', '2025-05-17 09:54:30', NOW(), NOW()),
    ('https://example.com/audio29.mp3', NULL, FALSE, '2025-05-17 09:55:00', '2025-05-17 09:56:00', NOW(), NOW()),
    ('https://example.com/audio30.mp3', 'End of session message.', TRUE, '2025-05-17 09:57:00', '2025-05-17 09:58:10', NOW(), NOW());
