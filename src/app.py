import os

from dotenv import load_dotenv
from flask import Flask

from routes.chat_routes import chat_bp
from routes.home_routes import home_bp

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.register_blueprint(chat_bp)
    app.register_blueprint(home_bp)

    return app
