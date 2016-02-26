import os


class BaseConfig:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'changeme')
    DB_NAME = os.environ.get('DB_NAME', '')
    DB_USER = os.environ.get('DB_USER', '')
    DB_PASS = os.environ.get('DB_PASS', '')
    DB_SERVICE = os.environ.get('DB_SERVICE', '')
    DB_PORT = os.environ.get('DB_PORT', '')
    #SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    #    DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
    #)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTHORIZATION_ENABLED = os.environ.get('AUTHORIZATION_ENABLED', True)
