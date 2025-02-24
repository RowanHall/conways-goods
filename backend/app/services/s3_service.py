from flask import request, jsonify, current_app
from app.extensions import s3
from config import ProductionConfig as Config
import uuid
from app.api.auth import get_current_user_service

def get_presigned_url_service():
    try:
        
        response, status_code = get_current_user_service()

        if status_code != 200:
            return status_code

        current_user_data = response.json

        current_user_id = current_user_data['user_id']
        current_user_role = current_user_data['user_role']
         
        if current_user_role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
            
        filename = request.args.get('filename')
        content_type = request.args.get('contentType')

        if not filename:
            return jsonify({'error': 'Filename is required'}), 400

        # Validate file extension
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        try:
            file_extention = filename.rsplit('.', 1)[1].lower()
            if file_extention not in allowed_extensions:
                return jsonify({'error': f'Invalid file type. Allowed types: {", ".join(allowed_extensions)}'}), 422
        except IndexError:
            return jsonify({'error': 'Invalid filename format'}), 422

        # Generate unique filename
        unique_filename = f"uploads/{current_user_id}/{uuid.uuid4()}.{file_extention}"

        # Generate presigned URL with minimal conditions
        presigned_post = s3.generate_presigned_post(
            Bucket=Config.BUCKET_NAME,
            Key=unique_filename,
            Fields={
                'Content-Type': content_type,
                'key': unique_filename,
                'bucket': Config.BUCKET_NAME
            },
            Conditions=[
                {'bucket': Config.BUCKET_NAME},
                {'key': unique_filename},
                ['content-length-range', 0, 10485760],  # 10MB max
                ['eq', '$Content-Type', content_type]
            ],
            ExpiresIn=3600  # 1 hour
        )

        return jsonify(presigned_post)

    except Exception as e:
        current_app.logger.error(f"Error generating presigned URL: {str(e)}")
        return jsonify({'error': str(e)}), 500