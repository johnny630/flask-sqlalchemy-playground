import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    # Session
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevelopmentConfig(BaseConfig):
    DEBUG = True

    # Flask-sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DB')

class ProductionConfig(BaseConfig):
    DEBUG = False

    # Flask-sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DB')

class TestingConfig(BaseConfig):
    TESTING = True

    # Flask-sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.db")

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}