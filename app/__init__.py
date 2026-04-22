import os
from flask import Flask
from dotenv import load_dotenv

from app.db import create_tables
from app.models import db
from app.routes import init_routes

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.getenv("SECRET_KEY") or "dev-secret-key"

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    os.makedirs(app.instance_path, exist_ok=True)

    db_path = os.path.join(app.instance_path, "students.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    create_tables(app)
    init_routes(app)

    return app