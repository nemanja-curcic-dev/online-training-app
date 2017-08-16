from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_login import LoginManager
from dateutil import tz

db = SQLAlchemy()
bootstrap = Bootstrap()
mail = Mail()
login_manager = LoginManager()


def return_app(type):
    app = Flask(__name__)
    app.config.from_object(config[type])

    db.init_app(app=app)
    bootstrap.init_app(app=app)
    mail.init_app(app=app)
    login_manager.init_app(app=app)

    login_manager.login_view = 'auth_blueprint.login'
    login_manager.session_protection = 'basic'
    login_manager.login_message = 'You must be logged in to see this page!'

    from .admin import admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .clients import clients_blueprint
    app.register_blueprint(clients_blueprint)

    return app


def utc_to_local(utc_dt):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    utc_dt = utc_dt.replace(tzinfo=from_zone)

    return utc_dt.astimezone(to_zone)