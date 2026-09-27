import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import CONFIGS


db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)

    environment = os.getenv("APP_ENV", "development").lower()
    config_class = CONFIGS.get(environment, CONFIGS["development"])
    app.config.from_object(config_class)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app