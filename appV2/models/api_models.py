"""
API 응답 모델
"""
from flask_restx import fields

def create_api_models(api):
    """API 모델 생성"""
    
    # 기본 작업 모델
    job_model = api.model('Job', {
        'record_id': fields.String(required=True, description='녹취록 ID'),
    })

    return {
        'job_model': job_model,
    }