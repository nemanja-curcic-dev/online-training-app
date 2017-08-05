import os


class Config:

    """Application configuration base class"""

    """Secret key"""
    SECRET_KEY = os.environ['SECRET_KEY']

    """Database and sqlalchemy set up"""
    mysql_username = os.environ['MYSQL_USERNAME']
    mysql_password = os.environ['MYSQL_PASSWORD']

    SQLALCHEMY_DATABASE_URI = 'mysql://' + mysql_username + ':' + mysql_password + '@localhost/online-training-app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """Email server set up"""
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'curesr@gmail.com'
    MAIL_PASSWORD = 'svedosmrtizajedno'


class DevelopmentConfig(Config):

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config = {
    'default': Config,
    'development': DevelopmentConfig
}