from dotenv import load_dotenv
import os

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@localhost:5433/test"
SQLALCHEMY_TRACK_MODIFICATIONS = False
