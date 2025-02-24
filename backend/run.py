 # Entry point for running Flask app
import os
from app import create_app
from config import ProductionConfig as Config


app = create_app(Config)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)