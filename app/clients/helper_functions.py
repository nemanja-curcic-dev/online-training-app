from app import db
from ..global_helpers import utc_now_to_timestamp
from ..models import Users, TrainingSession, TrainingSessionExercises, Exercises
from functools import wraps
from datetime import datetime
from flask_login import current_user
from flask import abort
from sqlalchemy import and_


def is_client(original_function):
    """Check if user is a client, if is, returns original function, else return 403 error(forbidden)"""
    @wraps(original_function)
    def wrapper(*args, **kwargs):
        user = Users.query.filter_by(id=current_user.id).first()

        if user:
            if not user.is_administrator:
                return original_function(*args, **kwargs)
            else:
                return abort(403)
        else:
            return abort(403)
    return wrapper


def client_training_sessions(id, new):
    new_trainings = []

    if new == 'new':
        training_sessions = TrainingSession.query.filter(and_(TrainingSession.user_id == id, TrainingSession.done == 0)).all()
    else:
        training_sessions = TrainingSession.query.filter(TrainingSession.user_id == id).all()

    for tr in training_sessions:
        new_trainings.append({
            'created': utc_now_to_timestamp(str(tr.date_created)), 'exercises':
            [ex.to_json() for ex in TrainingSessionExercises.query.filter_by(training_session_id=tr.id).all()],
            'id': tr.id
        })

    new_trainings.sort(key=lambda x: x['created'])

    return new_trainings


def exercise_by_name(name):
    exercise = Exercises.query.filter_by(name=name).first()

    return exercise.to_json()


def training_session_by_id(id):
    training = TrainingSession.query.get(id)
    exercises = []

    for exercise in [ex.to_json() for ex in training.exercises]:
        desc = exercise_by_name(exercise.get('exercise'))

        exercises.append({
          'exercise': exercise,
          'desc': desc
        })

    return exercises


def submit_training_data(data):
    evaluation = {
      'easy': 1,
      'right': 2,
      'hard': 3,
      'too_hard': 4
    }

    try:
        training_session = TrainingSession.query.get(data.get('training_id'))

        # update training session
        training_session.done = True
        training_session.date_done = datetime.utcnow()

        # update session exercises
        for k, mark in data.get('evaluated').items():
            print(k, mark)
            exercise = TrainingSessionExercises.query.get(k)
            exercise.mark = evaluation[mark]
            db.session.add(exercise)

        db.session.add(training_session)
        db.session.commit()
        return True
    except Exception:
      return False
