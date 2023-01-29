# Basic configuration: Production/Development/Testing
# Depreciated: replaced by using Flask-DotEnv 
import os
from os import environ
class Config(object):    
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    SESSION_COOKIE_NAME = "session"
    PERMANENT_SESSION_LIFETIME = 24 * 60 * 60
class ProductionConfig(Config):
    FLASK_ENV = "production"
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    PERMANENT_SESSION_LIFETIME = 1 * 60 * 60
    SQLALCHEMY_TRACK_MODIFICATIONS = True
class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
class TestingConfig(Config):
    FLASK_ENV = "testing"