from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def return_app(type):
    app = Flask(__name__)
    app.config.from_object(config[type])

    db.init_app(app=app)

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
