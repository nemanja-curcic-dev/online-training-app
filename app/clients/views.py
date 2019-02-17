import json

from flask import render_template, flash, request
from . import clients_blueprint
from ..models import Users
from flask_login import login_required, current_user
from app import db
from .helper_functions import is_client, client_training_sessions,\
  exercise_by_name, training_session_by_id, submit_training_data


@clients_blueprint.before_request
@login_required
@is_client
def before_request():
    if current_user.is_authenticated:
        user = Users.query.filter_by(id=current_user.id).first()

        if user:
            user.seen()

        if user.has_new_training:
            flash('You have a new training! You can check it out in training category!')
            user.has_new_training = False
            db.session.add(user)
            db.session.commit()


@clients_blueprint.route('/clients')
@login_required
@is_client
def profile():
    # tests = Tests.query.filter_by(alone=True).all()
    # users_tests = []
    #
    # if len(current_user.tests) != 0:
    #     users_tests = current_user.tests
    #     users_tests = filter(lambda x: x in tests, users_tests)

    return render_template('clients/profile.html', user=current_user)


@clients_blueprint.route('/clients/training/new_training')
@login_required
@is_client
def new_training():
    return render_template('clients/training/new_training.html', user=current_user)


@clients_blueprint.route('/clients/training/training_history')
@login_required
@is_client
def training_history():
    return render_template('clients/training/training_history.html', user=current_user)


@clients_blueprint.route('/clients/tests')
@login_required
@is_client
def tests():
    return render_template('clients/tests.html', user=current_user)


@clients_blueprint.route('/clients/do_training/')
@login_required
@is_client
def do_training():
    return render_template('clients/training/do_training.html', user=current_user)


@clients_blueprint.route('/clients/statistics/')
@login_required
@is_client
def statistics():
    return render_template('clients/statistics.html', user=current_user)


# ------------------------------ api methods ----------------------------------- #


@clients_blueprint.route('/clients/training_sessions/')
@login_required
@is_client
def get_training_sessions():
    return json.dumps(client_training_sessions(current_user.id, request.args.get('new')))


@clients_blueprint.route('/clients/exercise_by_name/')
@login_required
@is_client
def get_exercise_by_nanm():
    return json.dumps(exercise_by_name(request.args.get('name')))


@clients_blueprint.route('/clients/training_session_by_id/')
@login_required
@is_client
def get_training_session_by_id():
    return json.dumps(training_session_by_id(request.args.get('training_id')))


@clients_blueprint.route('/submit_training', methods=['POST'])
@login_required
def submit_training():
    if submit_training_data(request.json):
        return json.dumps({'status': True})
    return json.dumps({'status': False})
