from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    #"""Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    user = environ["MYSQL_USER"]
    password = environ["MYSQL_PASSWORD"]
    host = environ["MYSQL_HOST"]
    database = environ["MYSQL_DATABASE"]

    #DATABASE_CONNECTION_URI = f'mariadb+mariadbconnector://{user}:{password}@{host}/{database}'
    SQLALCHEMY_DATABASE_URI = f'mysql://{user}:{password}@{host}/{database}'
    print("************************")
    print(SQLALCHEMY_DATABASE_URI)    
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
