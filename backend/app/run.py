 # Entry point for running Flask app
from app import create_app
from config import DevelopmentConfig as Config


app = create_app(Config)

if __name__ == '__main__':
    app.run(port=5005, debug=True)