from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from app.utils.db import get_db_connection
from app.extensions import s3
from config import DevelopmentConfig
import uuid

def get_presigned_url_service():
    try:
        current_user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT role FROM users WHERE id = %s', (current_user_id,))
        user = cur.fetchone()
        
        current_user_role = user[0]
        if not user or current_user_role != 'admin':
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
            Bucket=DevelopmentConfig.BUCKET_NAME,
            Key=unique_filename,
            Fields={
                'Content-Type': content_type,
                'key': unique_filename,
                'bucket': DevelopmentConfig.BUCKET_NAME
            },
            Conditions=[
                {'bucket': DevelopmentConfig.BUCKET_NAME},
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
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()