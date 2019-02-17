from . import api_blueprint
from flask import jsonify, request
from .logic import exercise_data, calendar_data, calendar_data_from_start, training_session_by_id, insert_results, get_test_history
from flask_login import login_required

import json


@api_blueprint.before_request
@login_required
def before_request():
    pass


@api_blueprint.route('/api/return_exercise_data', methods=['POST'])
def return_exercise_data():
    return jsonify(exercise_data(int(request.json['user_id']), request.json['ex']))


@api_blueprint.route('/api/calendar_data', methods=['POST'])
def return_calendar_data():
    return json.dumps(calendar_data(request.json['month'], request.json['year']))


@api_blueprint.route('/api/sessions_from_beginning', methods=['POST'])
def sessions_from_beginning():
    return json.dumps(calendar_data_from_start(request.json['user_id']))


@api_blueprint.route('/api/clients_training_session', methods=['POST'])
def clients_training_session():
    """Returns training session (exercises, reps, sets, resistance)"""
    return json.dumps(training_session_by_id(request.json['session_id']))


@api_blueprint.route('/api/tests/post_results', methods=['POST'])
def test_results():
    return json.dumps(insert_results(request.json['results'],
                                     request.json['user_id'],
                                     request.json['type']))


@api_blueprint.route('/api/test_history', methods=['POST'])
def test_history():
    return json.dumps(get_test_history(request.json.get('user_id')))
