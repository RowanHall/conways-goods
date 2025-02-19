# Authentication API routes

from flask import Blueprint, request
from ..services.auth_service import login_service, register_service, get_current_user_service
from flask_jwt_extended import jwt_required
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    return login_service(data)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    return register_service(data)


@auth_bp.route('/api/me', methods=['GET'])
@jwt_required()
def get_current_user():
    return get_current_user_service()
