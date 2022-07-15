from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

'''
    Paso de la configuración a la app y creación de la app Flask.
    Inicialización de la base de datos mediante create_all para que
    se verifique la creación inicial de los modelos ORM con SqlAlchemy.
    
'''
def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
