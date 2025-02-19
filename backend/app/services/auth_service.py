# Handles authentication logic
from flask import jsonify
from app.utils.db import get_db_connection
from bcrypt import hashpw, checkpw, gensalt
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt

def login_service(data):
        username = data.get('username')
        password = data.get('password')

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Query user with role
            cur.execute('SELECT id, password_hash, role FROM users WHERE username = %s', (username,))
            user = cur.fetchone()

            user_id = user[0]
            user_password = user[1]
            user_role = user[2]

            if user and checkpw(password.encode('utf-8'), user_password.encode('utf-8')):
                # Create identity as a string instead of a dict
                identity = str(user_id)  # Convert user ID to string
                access_token = create_access_token(identity=identity,
                                                    additional_claims={"role": user[2]})
                
                return jsonify({
                    'token': access_token,
                    'is_admin': user_role == 'admin',
                    'user_id': user_id
                }), 200
            return jsonify({'error': 'Invalid credentials'}), 401
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            return jsonify({'error': str(e)}), 500
        finally:
            cur.close()
            conn.close()

def register_service(data):
     
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role', 'user')

    if not all([username, password, email]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Hash the password using bcrypt
        password_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        
        # Insert new user
        cur.execute('''
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        ''', (username, email, password_hash, role))
        
        user_id = cur.fetchone()[0]
        conn.commit()
        
        return jsonify({'id': user_id, 'message': 'User created successfully'}), 201
        
    except Exception as e:
        conn.rollback()
        print(f"Registration error: {str(e)}")  # Add debugging
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

def get_current_user_service():
    user_id = get_jwt_identity()
    claims = get_jwt()
    user_role = claims.get("role")
    return jsonify({"user_id": user_id, "user_role": user_role}), 200