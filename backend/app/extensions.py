# Initializes Flask extensions (DB, CORS, JWT)
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import boto3
from botocore.config import Config as BotoCoreConfig
from config import DevelopmentConfig as Config

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

s3 = boto3.client('s3',
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    config=BotoCoreConfig(region_name=Config.AWS_REGION)
) 