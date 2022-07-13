# config.py
import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSITION_SCHEMA = {
        'type': 'object',
        'properties': {
            'houmer_id': {'type': 'number'},
            'longitude': {'type': 'number'},
            'latitude': {'type': 'number'},
            'date':{'type':'string', 'pattern':'^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$'}
        },
        'required': ['houmer_id','longitude', 'latitude', 'date']
    }

    HOUMER_SCHEMA = {
        'type':'object',
        'properties':{
            'name':{'type':'string'},
            'email':{'type':'string', 'format':'email'}
        },
        'required':['name', 'email']
    }

    HOUMER_VISIT_REAL_STATE_SCHEMA = {
        'type': 'object',
        'properties': {
            'houmer_id': {'type': 'number'},
            'real_state_id': {'type': 'number'},
            'start_date': {'type': 'string', 'pattern':'^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$'},
            'end_date': {'type': 'string', 'pattern':'^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$'}
        },
        'required': ['houmer_id', 'real_state_id', 'start_date', 'end_date']
    }

    REAL_STATE_SCHEMA = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'longitude': {'type': 'number'},
            'latitude': {'type': 'number'}
        },
        'required': ['name', 'longitude', 'latitude']
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://development:develop1981$_@localhost:3306/development"
    SECRET_KEY = "development"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

