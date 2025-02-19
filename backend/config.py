from dotenv import load_dotenv
import os

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@localhost:5433/test"
SQLALCHEMY_TRACK_MODIFICATIONS = False
BUCKET_NAME = os.getenv('BUCKET_NAME')
# Make sure this matches what you're using to generate tokens
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
