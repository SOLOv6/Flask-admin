import os

BASE_DIR = os.path.dirname(__file__)

class Config:
    """ Flask Config """
    SECRET_KEY = 'solov6'
    SESSION_COOKIE_NAME = 'solov6admin'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@3.39.180.133:3306/solodb?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        db_env = os.environ.get('SQLALCHEMY_DATABASE_URI')
        if db_env:
            self.SQLALCHEMY_DATABASE_URI = db_env


class DevelopmentConfig(Config):
    """ Flask Config for Dev """
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = None
    WTF_CSRF_ENABLED = False


class TestingConfig(Config):
    __test__ = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'test.db'))


class ProductionConfig(Config):
    """ Flask Config for Prod """
    pass