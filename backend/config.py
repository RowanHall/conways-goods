from dotenv import load_dotenv
import os
import datetime

load_dotenv()

class DevelopmentConfig:
    # Flask
    SECRET_KEY = os.getenv('DEV_JWT_SECRET_KEY')
    
    # Database
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DEV_DB_USERNAME')}:{os.getenv('DEV_DB_PASSWORD')}@{os.getenv('DEV_DB_HOST')}:5433/{os.getenv('DEV_DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USERNAME = os.getenv('DEV_DB_USERNAME')
    DB_PASSWORD = os.getenv('DEV_DB_PASSWORD')
    DB_HOST = os.getenv('DEV_DB_HOST')
    DB_NAME = os.getenv('DEV_DB_NAME')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('DEV_JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    
    # S3
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.getenv('DEV_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('DEV_AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('DEV_AWS_REGION')
    
    # PayPal
    PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
    PAYPAL_SECRET = os.getenv('PAYPAL_SECRET')
    PAYPAL_API = "https://api-m.sandbox.paypal.com"

class ProductionConfig:
        # Flask
    SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    
    # Database
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('PROD_DB_USERNAME')}:{os.getenv('PROD_DB_PASSWORD')}@{os.getenv('PROD_DB_HOST')}:5433/{os.getenv('PROD_DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USERNAME = os.getenv('PROD_DB_USERNAME')
    DB_PASSWORD = os.getenv('PROD_DB_PASSWORD')
    DB_HOST = os.getenv('PROD_DB_HOST')
    DB_NAME = os.getenv('PROD_DB_NAME')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    
    # S3
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    
    # PayPal
    PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
    PAYPAL_SECRET = os.getenv('PAYPAL_SECRET')
    PAYPAL_API = "https://api-m.sandbox.paypal.com"
