import psycopg2
from config import DevelopmentConfig

def get_db_connection(): #TODO: move to utils.py #MOVING: TO UTILS.PY
    conn = psycopg2.connect(
        dbname=DevelopmentConfig.DB_NAME,
        user=DevelopmentConfig.DB_USERNAME,
        password=DevelopmentConfig.DB_PASSWORD,
        host=DevelopmentConfig.DB_HOST
    )
    return conn
