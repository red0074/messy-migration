from flask import Flask
from app.db import get_db


def create_app():
    app = Flask(__name__)

    # Register blueprints
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    with app.app_context():
        db = get_db()

    return app
