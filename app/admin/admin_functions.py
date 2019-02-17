from ..api.logic import set_parser, rep_exercise_parser, weight_lifted_parser
from functools import wraps
from flask_login import current_user
from ..models import Users, MainMuscleGroups, SubMuscleGroups, Muscles, \
    TrainingSession, Exercises, TrainingSessionExercises
from flask import abort
import re
import datetime
from app import utc_to_local, db
from sqlalchemy.sql import text
from ..global_helpers import change_date_format


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


def load_data_before_request(g):
    clients = Users.query.count()
    exercises = Exercises.query.count()
    trainings = TrainingSession.query.count()
    latest_seen = Users.query.limit(5)

    g.seen = []

    for ls in latest_seen:
        if ls.last_seen:
            g.seen.append((ls.first_name, ls.last_name, ls.last_seen))

    g.seen.sort(key=lambda x: x[2], reverse=True)

    for index, el in enumerate(g.seen):
        name = ' '.join((el[0], el[1]))
        g.seen[index] = ', '.join([datetime.datetime.strftime(utc_to_local(el[2]), '%a %d %b %Y %H:%M:%S'), name])

    g.client_count = clients - 1
    g.exercises_count = exercises
    g.training_count = trainings


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


def training_parser(training):
    """Parses input from training table in the template create training"""
    rows = training.split('#')
    training_data = []

    for r in rows:
        data = r.split('|')
        training_data.append(data)

    return training_data


# training session data functions
def sessions_by_muscle_groups(user_id, muscle_group_ids):
    """Returns array of training sessions filtered by muscle groups"""
    training_sessions = TrainingSession.query.filter_by(user_id=user_id).all()

    if training_sessions is None:
        return training_sessions

    # return only training sessions that match ids in muscle_group_ids parameters
    training_sessions = list(filter(lambda x:
                                    True if set(muscle_group_ids) ==
                                    set([t.muscle_group_id for t in x.training_muscle_groups])
                                    else False, training_sessions))

    return training_sessions


def rep_parser(exercise):
    """Returns total number of reps done (sets x reps)"""
    reps = 0

    if re.search('\+', exercise.reps):
        numbers = exercise.reps.split('+')
        for num in numbers:
            if re.search('s', num):
                num = num.split('s')[0]
                reps += int(num) * set_parser(exercise)
            else:
                reps += int(num) * set_parser(exercise)
    elif re.search('s', exercise.reps):
        if re.search('x', exercise.reps):
            time = exercise.reps.split('s')[0]
            multiplier, res = time.split('x')
            reps = float(multiplier) * float(res)
        else:
            reps = int(exercise.reps.split('s')[0]) * set_parser(exercise)
            reps = str(reps)
    else:
        reps = int(exercise.reps) * set_parser(exercise)

    return reps


def total_weight_lifted(exercise, user_id):
    """Returns total weight lifted in one exercise (sets x reps x resistance)"""
    user = Users.query.filter_by(id=user_id).first()
    ex = Exercises.query.filter_by(name=exercise.exercise).first()

    if re.search('\+', exercise.reps):
        return round((weight_lifted_parser(exercise) / 2 + user.weight * ex.percentage_of_bodyweight) * \
                     int(rep_parser(exercise)), 2)

    return round((weight_lifted_parser(exercise) + user.weight * ex.percentage_of_bodyweight) *\
            int(rep_parser(exercise)), 2)


def training_session_data(user_id, training_session):
    """Returns dictionary that contains data about training session (weights, reps, sets)"""
    training_data = {'date': change_date_format(str(training_session.date_created), "%m-%d")}

    if training_session is None:
        return training_data

    # prepare keys in the dictionary that are muscle groups worked in training session
    for muscle_groups in training_session.training_muscle_groups:
        training_data[MainMuscleGroups.query.filter_by(id=muscle_groups.muscle_group_id).first().name] \
            = {'sets': 0, 'reps': 0, 'weight': 0, 'time': 0}

    for exercise in training_session.exercises:
        ex = Exercises.query.filter_by(name=exercise.exercise).first()

        iterator = 0

        # prevents that keys that are not in dictionary appear
        while ex.muscles[iterator].sub_muscle_group.main_muscle_group.name not in training_data.keys():
            iterator += 1

        key = ex.muscles[iterator].sub_muscle_group.main_muscle_group.name

        # insert the data in the dictionary
        training_data[key]['sets'] += set_parser(exercise)

        if type(rep_parser(exercise)) is str:
            training_data[key]['time'] += int(rep_parser(exercise))
        elif type(rep_parser(exercise)) is int:
            training_data[key]['reps'] += int(rep_parser(exercise))

        training_data[key]['weight'] \
            += float(total_weight_lifted(exercise, user_id))

    return training_data


def multiple_sessions_data(user_id, muscle_group_ids):
    """Returns training data from multiple sessions"""
    training_sessions_data = []

    if len(muscle_group_ids) == 0:
        return training_sessions_data

    training_sessions = sessions_by_muscle_groups(user_id, muscle_group_ids)

    if not training_sessions:
        return training_sessions_data

    for tr_session in training_sessions:
        training_sessions_data.append(training_session_data(user_id, tr_session))

    index = list(training_sessions_data[0].keys()).index('date')
    training_sessions_data.sort(key=lambda x: x[list(x.keys())[index]], reverse=True)

    return training_sessions_data


def get_exercises_by_muscles(main_muscle_group_id):
    """Returns exercises for specific muscle group"""
    sub_muscle_groups = SubMuscleGroups.query.filter_by(main_muscle_group_id=main_muscle_group_id).all()
    muscles = []
    exercises = []
    data = []
    data_dict = {}

    for s in sub_muscle_groups:
        muscles += Muscles.query.filter_by(sub_muscle_group_id=s.id).all()

    sql_statement = "SELECT exercises.name, exercises.type FROM exercises, exercises_muscles \
                     WHERE exercises.id = exercises_muscles.exercise_id \
                     AND exercises_muscles.muscle_id = :muscle_id AND exercises_muscles.priority = 10"

    for m in muscles:
        exercises.append([p for p in db.engine.execute(text(sql_statement), muscle_id=m.id)])

    for ex in exercises:
        data += [[e[0], e[1]] for e in ex]

    for d in data:
        if d[0] not in data_dict:
            data_dict[d[0]] = d[1]
        else:
            pass

    return data_dict


def get_records_for_exercise(exercise, type_of, client_id):
    training_sessions = TrainingSession.query.filter_by(user_id=client_id).all()
    exercises = []
    exercise = exercise.strip('')
    data = []
    return_data = {}

    for session in training_sessions:
        ex = TrainingSessionExercises.query.\
             filter(TrainingSessionExercises.training_session_id == session.id,
                   TrainingSessionExercises.exercise == exercise).first()
        if ex:
            exercises.append(ex)

    if type_of == 1:
        pass
    elif type_of == 2:
        return_data["type_2"] = []
        for e in exercises:
            print("exercise: ", e.reps)
            if re.search('\+', e.reps):
                data.append((e.resistance, rep_exercise_parser(e) * weight_lifted_parser(e) / 2))
            else:
                data.append((e.resistance, rep_exercise_parser(e) * weight_lifted_parser(e)))
        data.sort(key=lambda x: x[0], reverse=True)
        return_data["type_2"].append(data[0][0])
        data.sort(key=lambda x: x[1], reverse=True)
        return_data["type_2"].append(str(data[0][1])+"kg")
    elif type_of == 3:
        pass

    return return_data




