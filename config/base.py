import logging


class BaseConfig:
    LOGGING_LEVEL = logging.INFO
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/graphverter'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET = 'secret'
    ACCESS_TOKEN_LIFETIME = 60 * 60 * 24 * 7  # 1 week
