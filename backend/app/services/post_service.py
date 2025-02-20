from flask import request, jsonify, make_response
from app.utils.db import get_db_connection
from flask_jwt_extended import get_jwt_identity
from app.extensions import s3
from config import DevelopmentConfig
from flask import current_app
from app.services.auth_service import get_current_user_service
def post_previewer_service():
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
        print(f"Error in post_previewer_service: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

def get_post_service(post_id):

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

def create_post_service():
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
            data.get('category').lower(),
            data.get('designer').lower()
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

def delete_post_service(post_id):
    try:
        response, status_code = get_current_user_service()

        if status_code != 200:
            return status_code

        current_user_data = response.json

        current_user_id = current_user_data['user_id']
        current_user_role = current_user_data['user_role']
        
        conn = get_db_connection()
        cur = conn.cursor()

        # 1. Check if the post exists and belongs to the current user
        cur.execute('SELECT user_id FROM posts WHERE id = %s', (post_id,))
        post_tuple = cur.fetchone()

        if not post_tuple:
            return jsonify({'error': 'Post not found'}), 404

        post_user_id = post_tuple[0]
        current_user_id = int(current_user_id)

        if post_user_id != current_user_id and current_user_role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

        # 2. Fetch the associated image URLs from post_image
        cur.execute('SELECT url FROM post_image WHERE posts_id = %s', (post_id,))
        image_rows = cur.fetchall()  # each row is a tuple, e.g. (url_value,)

        # 3. Delete each image from S3
        for row in image_rows:
            image_url = row[0]
            try:
                # Parse out the S3 key from the image URL (assuming .amazonaws.com/ is in the URL)
                key = image_url.split('.amazonaws.com/')[1]
                s3.delete_object(
                    Bucket=DevelopmentConfig.BUCKET_NAME,
                    Key=key
                )
            except Exception as e:
                current_app.logger.error(f"Error deleting S3 object: {str(e)}")

        # 4. Delete image records from post_image
        cur.execute('DELETE FROM post_image WHERE posts_id = %s', (post_id,))

        # 5. Finally, delete the post itself
        cur.execute('DELETE FROM posts WHERE id = %s', (post_id,))
        conn.commit()

        return jsonify({'message': 'Post deleted successfully'}), 200

    except Exception as e:
        if conn:
            conn.rollback()
        current_app.logger.error(f"Error deleting post: {str(e)}")
        return jsonify({'error': str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()