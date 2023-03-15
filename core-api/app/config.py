import os
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'JHS(UHA(S!JWHJ!HOJHASAS'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")  # PRD
    BASIC_AUTH_FORCE = os.getenv('BASIC_AUTH_FORCE', '1') == '0'
