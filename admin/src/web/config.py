"""
Módulo de configuración de los diferentes environments.
"""
from os import environ


class Config(object):
    """
    Configuración base.
    """
    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"
    JJSON_SORT_KEYS = False
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ALGORITHM = "HS256"
    JWT_SECRET_KEY="1234567890123456790"
    JWT_ACCESS_COOKIE_NAME="access_token_cookie"
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'None'
    JWT_COOKIE_CSRF_PROTECT = False
    GOOGLE_CLIENT_ID = "621808232668-dhucnvsri6mnf430g1u5p9n6p6agnhi9.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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"



class ProductionConfig(Config):
    """
    Configuración para production.
    """
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'leafcompanysoftware@gmail.com'
    MAIL_PASSWORD = 'dgijsifzwvpiprvq'

class DevelopmentConfig(Config):
    """
    Configuración para development.
    """
    DB_USER = environ.get("PDS_DB_USER")
    DB_PASS = environ.get("PDS_DB_PASS")
    DB_HOST = environ.get("PDS_DB_HOST")
    DB_NAME = environ.get("PDS_DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")



class TestingConfig(Config):
    """
    Configuración para testing.
    """
    TESTING = True


configs = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig
}
