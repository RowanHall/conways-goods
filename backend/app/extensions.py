# Initializes Flask extensions (DB, CORS, JWT)
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import boto3
from botocore.config import Config as BotoCoreConfig
from config import DevelopmentConfig

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

s3 = boto3.client('s3',
    aws_access_key_id=DevelopmentConfig.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=DevelopmentConfig.AWS_SECRET_ACCESS_KEY,
    config=BotoCoreConfig(region_name=DevelopmentConfig.AWS_REGION)
) 