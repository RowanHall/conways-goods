from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
import os


app = Flask(__name__)
# Enable CORS for all routes and all origins
# change for production
# CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
CORS(app)

app.config.from_object('config')

db = SQLAlchemy(app)

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
    query = """
        SELECT
            p.title,
            p.price,
            pi.url AS first_image_url,
            p.id
        FROM posts p
        LEFT JOIN post_image pi
            ON p.id = pi.posts_id
        WHERE pi.order_num = 1;
    """
    try:
        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Execute the query
        cur.execute(query)
        results = cur.fetchall()

        # Convert results into a list of dictionaries
        data = [
            {"title": row[0], "price": row[1], "first_image_url": row[2], "id": row[3]}
            for row in results
        ]

        # Clean up
        cur.close()
        conn.close()

        return data

    except psycopg2.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}



@app.route('/posts/first-image', methods=['GET'])
def get_posts_with_images():
    data = get_first_image_of_posts()
    return jsonify(data)

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
        
        # Query the database for the post with the given ID and its images
        cursor.execute(query, (post_id,))
        results = cursor.fetchall()

        if results:
            # Initialize post data with the first row
            post_data = {
                'id': results[0][0],
                'title': results[0][1],
                'price': results[0][2],
                'images': []
            }

            # Add images to the post data
            for row in results:
                if row[3]:  # Check if image_url is not None
                    post_data['images'].append(row[3])

    finally:
        cursor.close()
        conn.close()
        return jsonify(post_data), 200
        
 
if __name__ == "__main__":
    app.run(debug=True, port=5005)