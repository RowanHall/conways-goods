# Post API routes

from flask import Blueprint, request
from app.services.post_service import post_previewer_service, get_post_service, create_post_service
from flask_jwt_extended import jwt_required, get_jwt_identity
posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts/first-image', methods=['GET'])
def post_previewer():
    post_previews = post_previewer_service()
    return post_previews

@posts_bp.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    return get_post_service(post_id)

@posts_bp.route('/api/posts/create', methods=['POST'])
@jwt_required()
def create_post():
    return create_post_service()
    