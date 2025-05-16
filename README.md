# AICC 서비스

## V1
- source myenv/bin/activate

## V2 
- source env/bin/activate
- uvicorn app.main:app --reload --host=0.0.0.0 --port=8081
- celery -A app.main.celery worker --loglevel=info
- celery -A app.main.celery flower --port=5555

