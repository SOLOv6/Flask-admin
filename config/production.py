import os
from dotenv import load_dotenv
from config.default import BASE_DIR


load_dotenv(os.path.join(BASE_DIR, '.env'))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:3306/{dbname}'.format(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    dbname=os.getenv('DB_NAME')
)

SQLALCHEMY_TRACK_MODIFICATIONS = False