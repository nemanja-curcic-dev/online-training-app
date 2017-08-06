from . import db
from datetime import datetime


#user class
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


#training session classes
class TrainingSession(db.Model):
    __tablename__ = 'training_session'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime())
    training_goal = db.Column(db.String(60))
    training_type = db.Column(db.Integer)
    session_exercises = db.relationship('TrainingSessionExercises', backref='training_session', lazy='dynamic')


class TrainingSessionExercises(db.Model):
    __tablename__ = 'training_session_exercises'

    id = db.Column(db.Integer, primary_key=True)
    training_session_id = db.Column(db.Integer, db.ForeignKey('training_session.id'))
    training_part = db.Column(db.SmallInteger)
    exercise = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)