from flask import render_template, abort, g, request, json, flash, jsonify
from . import admin_blueprint
from ..models import Users, MainMuscleGroups, SubMuscleGroups, Muscles, Exercises, Equipment, \
    TrainingSession, TrainingSessionExercises, TrainingSessionMuscleGroups
from flask_login import login_required, current_user
from app import db
from datetime import datetime as datetime_2
from .forms import AddExercise, CreateTraining, ClientsProfiles
from sqlalchemy.sql import text
from .admin_functions import is_admin, load_all_muscles, training_parser, multiple_sessions_data,\
    exercise_data, calendar_data, load_data_before_request, training_session_by_id


@admin_blueprint.before_request
@login_required
@is_admin
def before_request():
    """Sets number of clients, exercises, trainings done, and last time
    that users were seen in the flask.g object"""
    load_data_before_request(g=g)


@admin_blueprint.route('/admin')
def admin():
    """Checks if user is admin and returns admin template, else returns 404(not found)"""
    user = Users.query.filter_by(id=current_user.id).first()

    if user and user.is_administrator:
        return render_template('admin/admin.html', user=user,
                               client_count=g.client_count,
                               exercises_count=g.exercises_count,
                               training_count=g.training_count,
                               seen=g.seen)
    abort(404)


@admin_blueprint.route('/by_muscle_group', methods=['GET', 'POST'])
def by_muscle_group():
    """Returns exercises sorted by muscle group"""
    dict_muscles = load_all_muscles()

    return render_template('admin/by_muscle_group.html', dict_muscles=dict_muscles)


@admin_blueprint.route('/by_muscle_group_load_exercises', methods=['POST'])
def by_muscle_group_load_exercises():
    """Returns exercises sorted by equipment in ajax template 'by_group_exercises'"""
    muscle_id = request.form['id']
    exercises_muscles = {}
    exercises_muscles_final = {}

    muscle = Muscles.query.filter_by(id=muscle_id).first()
    exercises = muscle.exercises_muscles
    equipment = Equipment.query.all()
    equipment = [(eq, "".join(eq.name.split())) for eq in equipment]

    sql_statement = 'SELECT muscles.name, exercises_muscles.priority FROM muscles, exercises_muscles, exercises ' \
                    'WHERE exercises.id = :exercise_id AND muscles.id = exercises_muscles.muscle_id ' \
                    'AND exercises.id = exercises_muscles.exercise_id ' \
                    'ORDER BY exercises_muscles.priority DESC'

    for exercise in exercises:
        muscles_priorities = db.engine.execute(text(sql_statement), exercise_id=exercise.id)
        exercises_muscles[exercise] = [mp for mp in muscles_priorities]

    for key, values in exercises_muscles.items():
        for tup in values:
            if tup[0] == muscle.name and tup[1] == 10:
                exercises_muscles_final[key] = values

    return render_template('admin/ajax/by_group_exercises.html', exercises_muscles=exercises_muscles_final,
                           equipment=equipment, muscle_name=muscle.name)


@admin_blueprint.route('/add_exercise', methods=['GET', 'POST'])
def add_exercise():
    """Adds new exercise to the database"""
    form = AddExercise(request.form)

    dict_muscles = load_all_muscles()

    # dynamically add equipment choices
    equipment = [(eq.id, eq.name) for eq in Equipment.query.all()]
    form.equipment.choices = equipment

    if request.method == 'POST':
        # get input values from form
        id_priority = []
        exercise_name = form.exercise_name.data

        # check if exercise already exists in the database
        if Exercises.query.filter_by(name=exercise_name.lower()).first():
            flash('Exercise already exists in the database.')

            return render_template('admin/add_exercise.html',
                                   form=form,
                                   dict_muscles=dict_muscles)

        # parse muscle id's and their priorities
        for val in request.form.getlist('muscles'):
            id_priority.append((val.split('/')))

        # add exercise
        exercise = Exercises(name=form.exercise_name.data, mechanics=form.mechanics.data,
                             utility=form.utility.data, force=form.direction.data,
                             type=form.type.data, description=form.description.data,
                             instructions=form.instructions.data, equipment=form.equipment.data)

        db.session.add(exercise)
        db.session.commit()

        # get inserted exercise because of id
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


@admin_blueprint.route('/create_training', methods=['GET', 'POST'])
def create_training():
    """Creates new training session"""
    form = CreateTraining(request.form)

    # dynamically adds clients and muscle groups to dropdown lists
    clients = [(c.id, c.first_name + ' ' + c.last_name) for c in Users.query.filter(Users.is_administrator != 1)]
    muscle_groups = [(m.id, m.name.upper()) for m in MainMuscleGroups.query.all()]
    form.clients.choices = clients
    form.muscle_groups_checkbox.choices = muscle_groups

    if request.method == 'POST' and form.validate_on_submit():
        training_data = training_parser(form.training.data)
        training_data.pop()
        training_session = TrainingSession(user_id=form.clients.data,
                                           date_created=datetime_2.utcnow(),
                                           training_goal=form.training_goal.data,
                                           annotations=form.annotations.data)

        db.session.add(training_session)

        user = Users.query.filter_by(id=form.clients.data).first()
        user.has_new_training = True
        db.session.add(user)

        db.session.commit()

        training_session_id = TrainingSession.query.order_by(TrainingSession.id.desc()).first()

        training_exercises = []

        for row in training_data:
            training_exercises.append(TrainingSessionExercises(training_session_id=training_session_id.id,
                                                               ordinal_number=int(row[0].strip('.')),
                                                               sets=row[3],
                                                               reps=row[4],
                                                               exercise=row[1],
                                                               resistance=row[2]))
        db.session.add_all(training_exercises)

        for el in form.muscle_groups_checkbox.data:
            training_muscle_groups = TrainingSessionMuscleGroups(training_session_id=training_session_id.id,
                                                                 muscle_group_id=el)
            db.session.add(training_muscle_groups)

        db.session.commit()

        flash('Training session successfully stored.')
        return render_template('admin/create_training.html', form=form)

    return render_template('admin/create_training.html', form=form)


@admin_blueprint.route('/check_exercise', methods=['POST'])
def check_exercise():
    """Helper function, checks whether exercise typed in to the exercise table exists"""
    exercise = request.form['ex']
    return_val = 'not_found'

    found = Exercises.query.filter(Exercises.name.like(exercise + "%")).all()

    if found:
        return_val = 'found'

    return return_val


@admin_blueprint.route('/return_training_session_volumes', methods=['POST'])
def return_training_session_volumes():
    return jsonify(multiple_sessions_data(int(request.json['user_id']), [int(x) for x in request.json['muscle_ids']]))


@admin_blueprint.route('/return_exercise_data', methods=['POST'])
def return_exercise_data():
    return jsonify(exercise_data(int(request.json['user_id']), request.json['ex']))


@admin_blueprint.route('/add_sub_muscle_group', methods=['POST'])
def add_sub_muscle_group():
    id = request.form['id']
    sub_muscles = SubMuscleGroups.query.filter_by(main_muscle_group_id=int(id)).all()
    l = []

    for s in sub_muscles:
        l.append((str(s.id).upper(), s.name.upper()))

    return json.dumps(l)


@admin_blueprint.route('/choose_client', methods=['GET'])
def choose_client():
    form = ClientsProfiles(request.form)

    clients = [(c.id, c.first_name + ' ' + c.last_name) for c in Users.query.filter(Users.is_administrator != 1)]
    form.clients_profiles.choices = clients

    return render_template('admin/choose_client.html', form=form)


@admin_blueprint.route('/clients_profiles', methods=['GET'])
def clients_profiles():
    user_id = request.args.get('clients_profiles')

    client = Users.query.filter_by(id=user_id).first()
    total_trainings_done = TrainingSession.query.filter_by(user_id=user_id).count()
    muscle_groups = MainMuscleGroups.query.all()
    muscles = muscle_groups.sub_muscle

    return render_template('admin/clients_profiles.html',
                           client=client,
                           trainings_done=total_trainings_done,
                           muscle_groups=muscle_groups)


@admin_blueprint.route('/clients_training_session', methods=['POST'])
def clients_training_session():
    """Returns training session (exercises, reps, sets, resistance)"""
    return json.dumps(training_session_by_id(request.json['session_id']))


@admin_blueprint.route('/calendar_data', methods=['POST'])
def return_calendar_data():
    return json.dumps(calendar_data(request.json['month'], request.json['year']))


# error handlers
@admin_blueprint.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403
