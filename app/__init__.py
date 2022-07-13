from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
