import os


class Config:

    """Application configuration base class"""

    """Secret key"""
    SECRET_KEY = os.environ['SECRET_KEY']

    """Database and sqlalchemy set up"""
    mysql_username = os.environ['MYSQL_USERNAME']
    mysql_password = os.environ['MYSQL_PASSWORD']

    SQLALCHEMY_DATABASE_URI = 'mysql://' + mysql_username + ':' + \
                              mysql_password + '@localhost/online_training_app?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config = {
    'default': Config,
    'development': DevelopmentConfig
}
