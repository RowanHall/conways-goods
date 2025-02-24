# Initializes Flask app & registers Blueprints
from flask import Flask
from .extensions import db, jwt, cors
from .api.auth import auth_bp
from .api.posts import posts_bp
from .api.s3 import s3_bp
from .api.payments import payments_bp
from config import ProductionConfig as Config

def create_app(config_object=None):
    app = Flask(__name__)
    
    # Load config
    if config_object:
        app.config.from_object(config_object)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={
        r"/*": {
            "origins": [Config.FRONTEND_URL],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(s3_bp)
    app.register_blueprint(payments_bp)
    
    return app