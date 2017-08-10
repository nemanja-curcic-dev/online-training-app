from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()


def return_app(type):
    app = Flask(__name__)
    app.config.from_object(config[type])

    db.init_app(app=app)
    bootstrap.init_app(app=app)

    from .admin import admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
