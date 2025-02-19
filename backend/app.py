from flask import Flask, jsonify, make_response, request
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
import os
import requests
import bcrypt
from bcrypt import hashpw, checkpw, gensalt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
import boto3
from botocore.config import Config
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)

CORS(app, resources={
    #change origin for production
    r"/*": {
        "origins": ["http://localhost:5173"],  # Your frontend origin
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname="test",
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        host="localhost"
    )
    return conn

app.config.from_object('config')

db = SQLAlchemy(app)

# Add PayPal configuration
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "YOUR_PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", "YOUR_PAYPAL_SECRET")
PAYPAL_API = "https://api-m.sandbox.paypal.com"  # Use "https://api-m.paypal.com" for production

# Add these configurations
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
jwt = JWTManager(app)

# S3 Configuration
s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config=Config(region_name=os.getenv('AWS_REGION'))
)
BUCKET_NAME = os.getenv('BUCKET_NAME')

def get_first_image_of_posts():
    base_query = """
        SELECT
            p.title,
            p.price,
            pi.url AS first_image_url,
            p.id
        FROM posts p
        LEFT JOIN post_image pi
            ON p.id = pi.posts_id
        WHERE pi.order_num = 1
    """
    conditions = []
    params = []
    
    # Get filter parameters from request URL
    min_price = request.args.get('minPrice')
    max_price = request.args.get('maxPrice')
    category = request.args.get('category')
    designer = request.args.get('designer')
    
    try:
        # Price filters
        if min_price and min_price.strip():
            conditions.append("p.price >= %s")
            params.append(float(min_price))
        if max_price and max_price.strip():
            conditions.append("p.price <= %s")
            params.append(float(max_price))
            
        # Category filter
        if category and category != 'all':
            conditions.append("p.category = %s")
            params.append(category)
            
        # Designer filter
        if designer and designer != 'all':
            conditions.append("p.designer = %s")
            params.append(designer)
            
    except ValueError:
        pass
    
    # Add conditions to base query if any filters are applied
    if conditions:
        base_query += " AND " + " AND ".join(conditions)

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if params:
            cur.execute(base_query, params)
        else:
            cur.execute(base_query)
        results = cur.fetchall()

        data = [
            {
                "title": row[0],
                "price": float(row[1]),
                "first_image_url": row[2],
                "id": row[3]
            }
            for row in results
        ]
        
        return jsonify(data)
    except Exception as e:
        print(f"Error in get_first_image_of_posts: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

def get_paypal_access_token():
    """ Get an access token from PayPal """
    auth = (PAYPAL_CLIENT_ID, PAYPAL_SECRET)
    response = requests.post(
        f"{PAYPAL_API}/v1/oauth2/token",
        auth=auth,
        data={"grant_type": "client_credentials"}
    )
    return response.json().get("access_token")

@app.route('/posts/first-image', methods=['GET'])
def get_posts_with_images():
    data = get_first_image_of_posts()
    return data

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, price FROM products;')  # Fetch name and price
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Convert rows to JSON-friendly format
    products = [{"name": row[0], "price": row[1]} for row in rows]
    return jsonify(products)

@app.route('/api/test', methods=['GET'])
def test():
    return {"message": "CORS is enabled!"}

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    query = """
        SELECT
            p.id,
            p.title,
            p.price,
            p.description,
            pi.url AS image_url
        FROM posts p
        LEFT JOIN post_image pi
            ON p.id = pi.posts_id
        WHERE p.id = %s
        ORDER BY pi.order_num;
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(query, (post_id,))
        results = cursor.fetchall()

        if results:
            post_data = {
                'id': results[0][0],
                'title': results[0][1],
                'price': results[0][2],
                'description': results[0][3],
                'images': []
            }

            for row in results:
                if row[4]:  # Image URL is now at index 4
                    post_data['images'].append(row[4])

            return jsonify(post_data), 200
    except Exception as e:
        print(f"Error in get_post: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/paypal/capture", methods=["POST"])
def capture_payment():
    """ Capture PayPal payment """
    try:
        data = request.json
        order_id = data.get("orderID")
        
        if not order_id:
            return jsonify({"error": "No order ID provided"}), 400

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_paypal_access_token()}"
        }
        
        response = requests.post(
            f"{PAYPAL_API}/v2/checkout/orders/{order_id}/capture",
            headers=headers
        )
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def hash_password(password: str) -> bytes:
    return hashpw(password.encode('utf-8'), gensalt())

def check_password(plain_password, stored_hash):
    return bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash.encode('utf-8'))

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Query user with role
        cur.execute('SELECT id, password_hash, role FROM users WHERE username = %s', (username,))
        user = cur.fetchone()
        
        if user and checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            # Create identity as a string instead of a dict
            identity = str(user[0])  # Convert user ID to string
            access_token = create_access_token(identity=identity)
            
            return jsonify({
                'token': access_token,
                'is_admin': user[2] == 'admin',
                'user_id': user[0]
            }), 200
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200

@app.route('/api/posts/create', methods=['POST'])
@jwt_required()
def create_post():
    # Add CORS headers explicitly for this endpoint
    def corsify_response(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response

    # Handle OPTIONS request (preflight)
    if request.method == 'OPTIONS':
        response = make_response()
        return corsify_response(response)

    current_user = get_jwt_identity()
    
    if not current_user:
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.json
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            INSERT INTO posts (title, price, description, user_id, category, designer)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            data['title'],
            data['price'],
            data.get('description', ''),
            current_user,  # Use the user ID directly
            data.get('category'),
            data.get('designer')
        ))
        
        post_id = cur.fetchone()[0]
        conn.commit()
        
        # Handle image URLs if provided
        if 'images' in data:
            for idx, image_url in enumerate(data['images']):
                cur.execute('''
                    INSERT INTO post_image (posts_id, url, order_num)
                    VALUES (%s, %s, %s)
                ''', (post_id, image_url, idx + 1))
            conn.commit()
            
        response = jsonify({'id': post_id})
        return corsify_response(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
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

@app.route('/api/s3/presigned-url', methods=['GET'])
@jwt_required()
def get_presigned_url():
    try:
        current_user_id = get_jwt_identity()
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT role FROM users WHERE id = %s', (current_user_id,))
        user = cur.fetchone()
        
        if not user or user[0] != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
            
        filename = request.args.get('filename')
        content_type = request.args.get('contentType')

        if not filename:
            return jsonify({'error': 'Filename is required'}), 400

        # Validate file extension
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        try:
            ext = filename.rsplit('.', 1)[1].lower()
            if ext not in allowed_extensions:
                return jsonify({'error': f'Invalid file type. Allowed types: {", ".join(allowed_extensions)}'}), 422
        except IndexError:
            return jsonify({'error': 'Invalid filename format'}), 422

        # Generate unique filename
        unique_filename = f"uploads/{current_user_id}/{uuid.uuid4()}.{ext}"

        # Generate presigned URL with minimal conditions
        presigned_post = s3.generate_presigned_post(
            Bucket=BUCKET_NAME,
            Key=unique_filename,
            Fields={
                # 'acl': 'public-read',
                'Content-Type': content_type,
                'key': unique_filename,
                'bucket': BUCKET_NAME
            },
            Conditions=[
                # {'acl': 'public-read'},
                {'bucket': BUCKET_NAME},
                {'key': unique_filename},
                ['content-length-range', 0, 10485760],  # 10MB max
                ['eq', '$Content-Type', content_type]
            ],
            ExpiresIn=3600  # 1 hour
        )

        return jsonify(presigned_post)

    except Exception as e:
        app.logger.error(f"Error generating presigned URL: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/test-auth', methods=['GET'])
@jwt_required()
def test_auth():
    try:
        # Get the user identity from the token
        current_user_id = get_jwt_identity()
        
        # Log the identity for debugging
        app.logger.info(f"Current user ID: {current_user_id}, Type: {type(current_user_id)}")
        
        # Query the database to get user details
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT id, username, role FROM users WHERE id = %s', (current_user_id,))
        user = cur.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'message': 'Authentication successful',
            'user': {
                'id': user[0],
                'username': user[1],
                'is_admin': user[2] == 'admin'
            }
        }), 200
        
    except Exception as e:
        app.logger.error(f"Auth test error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    app.run(debug=True, port=5005)

