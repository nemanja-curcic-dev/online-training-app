from . import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    date_registered = db.Column(db.DateTime(), default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    is_administrator = db.Column(db.Boolean, default=False)