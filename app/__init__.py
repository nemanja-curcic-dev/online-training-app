from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def return_app():
    app = Flask(__name__)

    db.init_app(app=app)

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
