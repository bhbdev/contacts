import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    APP_NAME = 'Contacts'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///contacts.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 10
    SEED_DB = os.environ.get('SEED_DB') or False
    SEED_COUNT = os.environ.get('SEED_COUNT') or 25
    GCLOUD_API_KEY = os.environ.get('GCLOUD_API_KEY') or 'your-gcloud-api-key'
    
    
