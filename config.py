# App Config


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'hard to guess string'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/micha/Documents/Development/weatherWebApp/zip_code_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = "not stupid enough to commit to GitHub"
