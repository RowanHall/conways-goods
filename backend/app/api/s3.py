from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.services.s3_service import get_presigned_url_service

s3_bp = Blueprint('s3', __name__)

@s3_bp.route('/api/s3/presigned-url', methods=['GET'])
@jwt_required()
def get_presigned_url():
    return get_presigned_url_service()
    