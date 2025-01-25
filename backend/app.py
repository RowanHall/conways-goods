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
