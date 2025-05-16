import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'mysql'),
        user=os.getenv('MYSQL_USER', 'rootuser'),
        password=os.getenv('MYSQL_PASSWORD', 'rootpw'),
        database=os.getenv('MYSQL_DATABASE', 'aicc')
    )
