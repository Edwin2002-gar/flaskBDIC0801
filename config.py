import os 
from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY = "claveSecreta"
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = True 
    WTF_CSRF_TIME_LIMIT = None 
    
class DevelopmentConfig(Config):
    DEBUG = True
    # Cambiar pymysql por mysqlconnector
    SQLALCHEMY_DATABASE_URI ='mysql+mysqlconnector://EdwinGarcia:root@localhost:3306/ico801'
    SQLALCHEMY_TRACK_MODIFICATIONS = False