import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSITION_SCHEMA = {
        'type': 'object',
        'properties': {
            'houmer_id': {'type': 'number'},
            'longitude': {'type': 'number'},
            'latitude': {'type': 'number'},
            'date': {'type': 'string', 'pattern': '^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$'}
        },
        'required': ['houmer_id', 'longitude', 'latitude', 'date']
    }

    HOUMER_SCHEMA = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'email': {'type': 'string', 'format': 'email'}
        },
        'required': ['name', 'email']
    }

    HOUMER_VISIT_REAL_STATE_SCHEMA = {
        'type': 'object',
        'properties': {
            'houmer_id': {'type': 'number'},
            'real_state_id': {'type': 'number'},
            'start_date': {'type': 'string', 'pattern': '^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$'},
            'end_date': {'type': 'string', 'pattern': '^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$'}
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

    HOUMER_VISIT_COORDINATES_SCHEMA = {
        'type': 'object',
        'properties': {
            'houmer_id': {'type': 'number'},
            'date': {'type': 'string', 'pattern': '^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$'}
        },
        'required': ['houmer_id', 'date']
    }

    HOUMER_EXCEEDED_SPEED_SCHEMA = {
        'type': 'object',
        'properties': {
            'houmer_id': {'type': 'number'},
            'date': {'type': 'string', 'pattern': '^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$'},
            'max_speed': {'type': 'number'}
        },
        'required': ['houmer_id', 'date', 'max_speed']
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("HOUM_DEVELOPMENT_DATABASE_URI")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("HOUM_TESTING_DATABASE_URI")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("HOUM_PRODUCTION_DATABASE_URI")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
