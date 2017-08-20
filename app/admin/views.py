from flask import render_template, abort, g, request, json, flash
from . import admin_blueprint
from ..models import Users, MainMuscleGroups, SubMuscleGroups, Muscles, Exercises
from flask_login import login_required, current_user
from app import db, utc_to_local
from _datetime import datetime
from .forms import AddExercise
from sqlalchemy.sql import text
from functools import wraps


# helper functions
def is_admin(original_function):
    """Check if user is admin, if is, return original function, else return 403 error(forbidden)"""
    @wraps(original_function)
    def wrapper(*args, **kwargs):
        user = Users.query.filter_by(id=current_user.id).first()

        if user:
            if user.is_administrator:
                return original_function(*args, *kwargs)
            else:
                return abort(403)
        else:
            return abort(403)
    return wrapper


def load_all_muscles():
    """Returns dictionary with all main muscle groups, sub muscle groups and muscles"""
    main_muscle_groups = MainMuscleGroups.query.all()
    sub_muscle_groups = SubMuscleGroups.query.all()
    muscles = Muscles.query.all()
    dict_muscles = {}

    for main_muscle in main_muscle_groups:
        dict_muscles[main_muscle] = [sm for sm in sub_muscle_groups if sm.main_muscle_group_id == main_muscle.id]

    for key, value in dict_muscles.items():
        for index in range(len(dict_muscles[key])):
            sub_mus = dict_muscles[key][index]
            dict_muscles[key][index] = {sub_mus: [m for m in muscles if m.sub_muscle_group_id == sub_mus.id]}

    return dict_muscles


@admin_blueprint.before_request
@login_required
@is_admin
def before_request():
    """Sets number of clients, exercises, trainings done, and last time
    that users were seen in the flask.g object"""
    clients = db.engine.execute('SELECT COUNT(users.id) FROM users')
    exercises = db.engine.execute('SELECT COUNT(id) FROM exercises')
    trainings = db.engine.execute('SELECT COUNT(id) FROM training_session')
    latest_seen = db.engine.execute('SELECT first_name, last_name, last_seen FROM users LIMIT 5')

    g.seen = []

    for ls in latest_seen:
        if ls[2]:
            g.seen.append(ls)

    g.seen.sort(key=lambda x: x[2], reverse=True)

    for index, el in enumerate(g.seen):
        name = ' '.join((el[0], el[1]))
        g.seen[index] = ', '.join([datetime.strftime(utc_to_local(el[2]), '%a %d %b %Y %H:%M:%S'), name])

    for cl in clients:
        g.client_count = cl[0] - 1

    for ex in exercises:
        g.exercises_count = ex[0]

    for tr in trainings:
        g.training_count = tr[0]


@admin_blueprint.route('/admin/<id>')
@login_required
def admin(id):
    """Checks if user is admin and returns admin template, else returns 404(not found)"""
    user = Users.query.filter_by(id=id).first()

    if user and user.is_administrator:
        return render_template('admin/admin.html', user=user,
                               client_count=g.client_count,
                               exercises_count=g.exercises_count,
                               training_count=g.training_count,
                               seen=g.seen)
    abort(404)


@admin_blueprint.route('/by_muscle_group', methods=['GET', 'POST'])
@login_required
def by_muscle_group():
    """Returns exercises sorted by muscle group"""

    dict_muscles = load_all_muscles()

    return render_template('admin/by_muscle_group.html', dict_muscles=dict_muscles)


@admin_blueprint.route('/add_exercise', methods=['GET', 'POST'])
@login_required
@is_admin
def add_exercise():
    form = AddExercise(request.form)

    dict_muscles = load_all_muscles()

    if request.method == 'POST':
        #get input values from form
        id_priority = []
        exercise_name = form.exercise_name.data
        com_aux_iso = form.priority.data
        force = form.direction.data
        type = form.type.data

        #check if exercise already exists in the database
        if Exercises.query.filter_by(name=exercise_name.lower()).first():
            flash('Exercise already exists in the database.')

            return render_template('admin/add_exercise.html',
                                   form=form,
                                   dict_muscles=dict_muscles)

        #parse muscle id's and their priorities
        for val in request.form.getlist('muscles'):
            id_priority.append((val.split('/')))

        #add exercise
        exercise = Exercises(name=exercise_name, compound_isolated=com_aux_iso,
                             force=force, type=type)

        db.session.add(exercise)
        db.session.commit()

        #get inserted exercise because of id
        exercise = Exercises.query.filter_by(name=exercise_name).first()

        sql_statement = 'INSERT INTO exercises_muscles (exercise_id, muscle_id, priority) ' \
                        'VALUES (:exercise_id, :muscle_id, :priority)'

        for val in id_priority:
            db.engine.execute(text(sql_statement), exercise_id=exercise.id,
                              muscle_id=val[0], priority=val[1])

        flash('Exercise was successfully added to the database.')

        return render_template('admin/add_exercise.html',
                               form=form,
                               dict_muscles=dict_muscles)

    return render_template('admin/add_exercise.html',
                           form=form,
                           dict_muscles=dict_muscles)


@admin_blueprint.route('/add_sub_muscle_group', methods=['POST'])
@login_required
def add_sub_muscle_group():
    id = request.form['id']
    sub_muscles = SubMuscleGroups.query.filter_by(main_muscle_group_id=int(id)).all()
    l = []

    for s in sub_muscles:
        l.append((str(s.id).upper(), s.name.upper()))

    return json.dumps(l)


@admin_blueprint.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403
