from functools import wraps
from flask_login import current_user
from ..models import Users, MainMuscleGroups, SubMuscleGroups, Muscles, \
    TrainingSession, Exercises, TrainingSessionExercises
from flask import abort
import re
import datetime
import calendar
from app import utc_to_local


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


def set_parser(exercise):
    """Returns number of sets done for one exercise"""
    return int(exercise.sets)


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


def weight_lifted_parser(exercise):
    """Parses weight lifted"""
    weight = 0

    if re.search('/', exercise.resistance):
        pass
    elif re.search('x', exercise.resistance):
        multiplier, resistance = exercise.resistance.split('x')
        weight = float(multiplier) * float(resistance.split('k')[0])
    else:
        weight = float(exercise.resistance.split('k')[0])

    return weight


def total_weight_lifted(exercise, user_id):
    """Returns total weight lifted in one exercise (sets x reps x resistance)"""
    user = Users.query.filter_by(id=user_id).first()
    ex = Exercises.query.filter_by(name=exercise.exercise).first()

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

    for tr_session in training_sessions:
        training_sessions_data.append(training_session_data(user_id, tr_session))

    index = list(training_sessions_data[0].keys()).index('date')
    training_sessions_data.sort(key=lambda x: x[list(x.keys())[index]], reverse=True)

    return training_sessions_data


# exercise data functions
def rep_exercise_parser(exercise):
    reps = 0

    if re.search('\+', exercise.reps):
        numbers = exercise.reps.split('+')
        for num in numbers:
            if re.search('s', num):
                num = num.split('s')[0]
                reps += int(num)
            else:
                reps += int(num)
    elif re.search('s', exercise.reps):
        if re.search('x', exercise.reps):
            time = exercise.reps.split('s')[0]
            multiplier, res = time.split('x')
            reps = float(multiplier) * float(res)
        else:
            reps = int(exercise.reps.split('s')[0])
            reps = str(reps)
    else:
        reps = int(exercise.reps)

    return reps


def exercise_data(user_id, exercise_name):
    data_exercise = {}
    sessions = TrainingSession.query.filter_by(user_id=user_id).all()

    exercises = TrainingSessionExercises.query.\
        filter((TrainingSessionExercises.training_session_id.in_([s.id for s in sessions]))
               & (TrainingSessionExercises.exercise == exercise_name)).all()

    for ex in exercises:
        date = change_date_format(str(TrainingSession.query.
                                      filter_by(id=ex.training_session_id).first().date_created), "%m-%d")
        data_exercise[date] = [set_parser(ex), rep_exercise_parser(ex), weight_lifted_parser(ex)]

    return data_exercise


def calendar_data(month, year):
    """Returns data that is inserted in calendar (dates of trainings, training session ids, etc.)"""
    number_of_days = calendar.monthrange(year, month)
    first_day = datetime.date(year, month, 1).strftime("%Y-%m-%d %H:%M:%S")
    last_day = datetime.date(year, month, number_of_days[1]).strftime("%Y-%m-%d %H:%M:%S")
    data = {}

    training_sessions = TrainingSession.\
        query.filter(TrainingSession.date_created >= first_day, TrainingSession.date_created <= last_day).all()

    for tr in training_sessions:
        session_muscle_groups = tr.training_muscle_groups
        muscle_groups_names = MainMuscleGroups.query.\
            filter(MainMuscleGroups.id.in_([m.muscle_group_id for m in session_muscle_groups]))
        data[change_date_format(str(tr.date_created), "%a %b %d %Y")]\
            = (tr.id, [m.name for m in muscle_groups_names])

    return data


def training_session_by_id(session_id):
    training_session = TrainingSession.query.filter_by(id=session_id).first()
    exercises = training_session.exercises
    date = change_date_format(str(training_session.date_created), "%a %b %d %Y")

    training_session_exercises = []

    for ex in exercises:
        training_session_exercises\
            .append([ex.ordinal_number, ex.exercise, ex.resistance, ex.sets, ex.reps])

    return training_session_exercises


def change_date_format(date, format):
    """Returns adequate date format for chart representation"""
    return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime(format)



