from flask import render_template, abort, g, request, jsonify, json
from . import admin_blueprint
from ..models import Users, MainMuscleGroups, SubMuscleGroups, Muscles
from flask_login import login_required
from app import db, utc_to_local
from _datetime import datetime
from .forms import AddExercise


@admin_blueprint.before_request
@login_required
def before_request():
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
    user = Users.query.filter_by(id=id).first()

    if user is None:
        abort(404)

    return render_template('admin/admin.html', user=user,
                           client_count=g.client_count,
                           exercises_count=g.exercises_count,
                           training_count=g.training_count,
                           seen=g.seen)


@admin_blueprint.route('/by_muscle_group', methods=['POST'])
@login_required
def by_muscle_group():
    main_muscle_groups = MainMuscleGroups.query.all()
    sub_muscle_groups = []

    for main_muscle in main_muscle_groups:
        main_muscle.name = main_muscle.name.upper()
        sub_muscle_groups.append(SubMuscleGroups.query.filter_by(main_muscle_group_id=main_muscle.id).all())

    return render_template('admin/ajax_templates/by_muscle_group.html',
                           muscle_groups=main_muscle_groups, sub_muscle_groups=sub_muscle_groups)


@admin_blueprint.route('/add_exercise', methods=['POST'])
@login_required
def add_exercise():
    form = AddExercise(request.form)

    main_muscle_groups = MainMuscleGroups.query.all()
    sub_muscle_groups = SubMuscleGroups.query.all()
    muscles = Muscles.query.all()
    dict_muscles = {}

    if form.validate_on_submit():
        pass

    for main_muscle in main_muscle_groups:
        dict_muscles[main_muscle] = [sm for sm in sub_muscle_groups if sm.main_muscle_group_id == main_muscle.id]

    for key, value in dict_muscles.items():
        for index in range(len(dict_muscles[key])):
            sub_mus = dict_muscles[key][index]
            dict_muscles[key][index] = {sub_mus: [m for m in muscles if m.sub_muscle_group_id == sub_mus.id]}

    return render_template('admin/ajax_templates/add_exercise.html',
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
