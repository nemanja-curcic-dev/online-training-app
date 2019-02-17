from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from datetime import datetime


exercises_muscles = db.Table('exercises_muscles',
                             db.Column('exercise_id', db.Integer, db.ForeignKey('exercises.id')),
                             db.Column('muscle_id', db.Integer, db.ForeignKey('muscles.id')),
                             db.Column('priority', db.SmallInteger))


# class AnthropometryUsersTests(db.Model):
#     __tablename__ = 'anthropometry_users_tests'
#
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
#     test_id = db.Column(db.Integer, db.ForeignKey('anthropometry_tests.id'), primary_key=True)
#     date_done = db.Column(db.DateTime)
#     weight = db.Column(db.Integer)
#     waist = db.Column(db.Integer)
#     thigh = db.Column(db.Integer)
#     body_fat_percentage = db.Column(db.Integer)
#     body_fat_mass = db.Column(db.Integer)
#     muscle_mass_percentage = db.Column(db.Integer)
#     muscle_mass = db.Column(db.Integer)
#
#     # relationships
#     anthropometry_tests = db.relationship("AnthropometryTests", back_populates="users")
#     anthropometry_users = db.relationship("Users", back_populates="anthropometry_tests")


# user class
class Users(db.Model, UserMixin):
    """User class"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    date_registered = db.Column(db.DateTime(), default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    is_administrator = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    has_new_training = db.Column(db.Boolean, default=False)
    first_time = db.Column(db.Boolean, default=False)

    anthropometry_tests = db.relationship('AnthropometryTests', back_populates='user')

    def __init__(self, first_name='', last_name='', email='', password=''):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    @property
    def password(self):
        raise AttributeError('Password is read only property!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(pwhash=self.password_hash, password=password)

    def generate_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=1800)
        return s.dumps(self.email)

    @staticmethod
    def check_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            user_email = s.loads(token)
            user = Users.query.filter_by(email=user_email).first()
        except:
            return False

        if not user:
            return False

        user.confirmed = True
        db.session.add(user)
        db.session.commit()

        return True

    @staticmethod
    def from_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            user_email = s.loads(token)
        except:
            return None

        user = Users.query.filter_by(email=user_email).first()

        if user:
            return user

        return None

    def seen(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=int(user_id)).first()


# training session classes
class TrainingSession(db.Model):
    __tablename__ = 'training_session'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime())
    date_done = db.Column(db.DateTime())
    training_goal = db.Column(db.String(60))
    training_type = db.Column(db.Integer)
    annotations = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
          'id': self.id,
          'user_id': self.user_id,
          'training_goal': self.training_goal,
          'date_created': str(self.date_created),
          'training_type': self.training_type,
          'annotations': self.annotations,
          'done': self.annotations
        }


class TrainingSessionExercises(db.Model):
    __tablename__ = 'training_session_exercises'

    id = db.Column(db.Integer, primary_key=True)
    training_session_id = db.Column(db.Integer, db.ForeignKey('training_session.id'))
    exercise = db.Column(db.String(60))
    sets = db.Column(db.String(50))
    reps = db.Column(db.String(50))
    resistance = db.Column(db.String(40))
    ordinal_number = db.Column(db.SmallInteger)
    mark = db.Column(db.SmallInteger)  # 1 - easy, 2 - just right, 3 - hard, 4 - too hard
    session_exercises = db.relationship('TrainingSession', backref='exercises')

    def __repr__(self):
        return self.exercise

    def to_json(self):
        return {
            'id': self.id,
            'exercise': self.exercise.capitalize(),
            'sets': self.sets,
            'reps': self.reps,
            'resistance': self.resistance
        }


class TrainingSessionMuscleGroups(db.Model):
    __tablename__ = 'training_session_muscle_groups'

    id = db.Column(db.Integer, primary_key=True)
    training_session_id = db.Column(db.Integer, db.ForeignKey('training_session.id'))
    muscle_group_id = db.Column(db.Integer)
    session_muscle_groups = db.relationship('TrainingSession',
                                            backref='training_muscle_groups')


# exercises and muscle groups classes
class MainMuscleGroups(db.Model):
    __tablename__ = 'main_muscle_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    sub_muscle_groups = db.relationship('SubMuscleGroups', backref='main_muscle_group', lazy='select')

    def __repr__(self):
        return self.name.upper()


class SubMuscleGroups(db.Model):
    __tablename__ = 'sub_muscle_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    main_muscle_group_id = db.Column(db.Integer, db.ForeignKey('main_muscle_groups.id'))
    muscles = db.relationship('Muscles', backref='sub_muscle_group', lazy='dynamic')

    def __repr__(self):
        return self.name.upper()


class Muscles(db.Model):
    __tablename__ = 'muscles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    sub_muscle_group_id = db.Column(db.Integer, db.ForeignKey('sub_muscle_groups.id'))
    exercises_muscles = db.relationship('Exercises', secondary=exercises_muscles,
                                        backref=db.backref('exercises_muscles', lazy='dynamic'))

    def __repr__(self):
        return self.name.upper()


class Exercises(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # bodyweight = 1 ; weighted = 2  ; can be both = 3
    type = db.Column(db.SmallInteger)
    # basic = 1 ; auxilary = 2 ;
    utility = db.Column(db.SmallInteger)
    force = db.Column(db.String(5))
    # compound = 1 ; isolated = 2 ;
    mechanics = db.Column(db.SmallInteger)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    variation_of = db.Column(db.Integer)
    percentage_of_bodyweight = db.Column(db.Float, default=0.0)
    equipment = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    get_equipment = db.relationship('Equipment', backref='equipment', lazy='select')
    muscles = db.relationship('Muscles', secondary=exercises_muscles,
                              backref=db.backref('muscles', lazy='dynamic'),
                              order_by=exercises_muscles.columns.priority.desc)
    img_link = db.Column(db.String(64))
    video_description = db.Column(db.String(256))

    def __repr__(self):
        return self.name

    def to_json(self):
        return{
          'name': self.name.capitalize(),
          'description': self.description,
          'instructions': self.instructions,
          'img_link': self.img_link
        }


class Equipment(db.Model):
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return self.name.upper()


class AnthropometryTests(db.Model):
    __tablename__ = 'anthropometry_tests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    test_name = db.Column(db.String(100))
    test_category = db.Column(db.String(64))

    date_done = db.Column(db.DateTime)
    weight = db.Column(db.Integer)
    waist = db.Column(db.Integer)
    thigh = db.Column(db.Integer)
    body_fat_percentage = db.Column(db.Integer)
    body_fat_mass = db.Column(db.Integer)
    muscle_mass_percentage = db.Column(db.Integer)
    muscle_mass = db.Column(db.Integer)

    user = db.relationship("Users", back_populates="anthropometry_tests")

    def __repr__(self):
        return self.test_name

    def to_json(self):
        return {
          'id': self.id,
          'user_id': self.user_id,
          'test_name': self.test_name,
          'test_category': self.test_category,
          'date_done': str(self.date_done).split(' ')[0],
          'weight': self.weight,
          'waist': self.waist,
          'thigh': self.thigh,
          'body_fat_percentage': self.body_fat_percentage,
          'body_fat_mass': self.body_fat_mass,
          'muscle_mass_percentage': self.muscle_mass_percentage,
          'muscle_mass': self.muscle_mass
        }




