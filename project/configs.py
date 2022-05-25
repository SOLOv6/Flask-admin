import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    """ Flask Config """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:3306/{dbname}?charset=utf8'.format(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        db_env = os.environ.get('SQLALCHEMY_DATABASE_URI')
        if db_env:
            self.SQLALCHEMY_DATABASE_URI = db_env


class DevelopmentConfig(Config):
    """ Flask Config for Dev """
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = None


class TestingConfig(Config):
    __test__ = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'test.db'))


class ProductionConfig(Config):
    """ Flask Config for Prod """
    pass