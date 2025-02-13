from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes and all origins
# change for production
# CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
CORS(app)

app.config.from_object('config')

db = SQLAlchemy(app)

# Add PayPal configuration
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "YOUR_PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", "YOUR_PAYPAL_SECRET")
PAYPAL_API = "https://api-m.sandbox.paypal.com"  # Use "https://api-m.paypal.com" for production

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname="test",
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        host="localhost"
    )
    return conn

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

if __name__ == "__main__":
    app.run(debug=True, port=5005)