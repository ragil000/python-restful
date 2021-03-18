from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI')
    SQLALCHEMY_POOL_SIZE=20
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_SERVER = '127.0.0.1'
    SERVER_NAME = '127.0.0.1:3000'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    DB_SERVER = '127.0.0.1:5000'
    # SECRET_KEY = environ.get('API_FLASK_SECRET_KEY')
    # VAULT_ADDR = environ.get('VAULT_ADDR')
    # VAULT_TOKEN = environ.get('VAULT_TOKEN')

app_config_dict = {
    'Production': ProductionConfig,
    'Development': DevelopmentConfig
}