import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'test.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'keys/aiffel-gn3-2-035da204163f.json'