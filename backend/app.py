from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import psycopg2

from dotenv import load_dotenv
import os

app = Flask(__name__)

# Enable CORS for all routes and all origins
# change for production
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
            pi.url AS first_image_url
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
            {"title": row[0], "first_image_url": row[1]}
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

if __name__ == "__main__":
    app.run(debug=True)
