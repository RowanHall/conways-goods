import psycopg2
from config import ProductionConfig as Config

def get_db_connection(): #TODO: move to utils.py #MOVING: TO UTILS.PY
    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USERNAME,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST
    )
    return conn
