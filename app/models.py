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


#exercises and muscle groups classes
class MainMuscleGroups(db.Model):
    __tablename__ = 'main_muscle_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    sub_muscle_groups = db.relationship('SubMuscleGroups', backref='main_muscle_group', lazy='dynamic')


class SubMuscleGroups(db.Model):
    __tablename__ = 'sub_muscle_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    main_muscle_group_id = db.Column(db.Integer, db.ForeignKey('main_muscle_groups.id'))
    muscles = db.relationship('Muscles', backref='sub_muscle_group', lazy='dynamic')


exercises_muscles = db.Table('exercises_muscles',
                             db.Column('exercise_id', db.Integer, db.ForeignKey('exercises.id')),
                             db.Column('muscle_id', db.Integer, db.ForeignKey('muscles.id')),
                             db.Column('priority', db.SmallInteger))


class Muscles(db.Model):
    __tablename__ = 'muscles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    sub_muscle_group_id = db.Column(db.Integer, db.ForeignKey('sub_muscle_groups.id'))
    exercises_muscles = db.relationship('Exercises', secondary=exercises_muscles,
                                        backref=db.backref('exercises_muscles', lazy='dynamic'))

    def __repr__(self):
        return self.name


class Exercises(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.SmallInteger) #bodyweight = 1 ; weighted = 2  ; can be both = 3
    force = db.Column(db.String(5))
    compound_isolated = db.Column(db.SmallInteger) #compound = 1 ; auxilary = 2 ;isolated = 3

    def __repr__(self):
        return self.name
