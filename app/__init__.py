import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Set secret key from .env
    app.secret_key = os.getenv("SECRET_KEY")

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
