from app import db
from dateutil.relativedelta import relativedelta
from ..models import TrainingSession, TrainingSessionExercises, Exercises, Users, MainMuscleGroups, AnthropometryTests
from ..global_helpers import change_date_format

import calendar
import datetime
import re


def set_parser(exercise):
    """Returns number of sets done for one exercise"""
    return int(exercise.sets)


# exercise data functions
def rep_exercise_parser(exercise):
    """Returns number of reps done in one exercise"""
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


def exercise_data(user_id, exercise_name):
    data_exercise = {}
    sessions = TrainingSession.query.filter_by(user_id=user_id).all()

    exercise = Exercises.query.filter_by(name=exercise_name).first()
    user = Users.query.get(user_id)
    print(user.weight)

    exercises = TrainingSessionExercises.query.\
        filter((TrainingSessionExercises.training_session_id.in_([s.id for s in sessions]))
               & (TrainingSessionExercises.exercise == exercise_name)).all()

    for ex in exercises:
        date = change_date_format(str(TrainingSession.query.
                                      filter_by(id=ex.training_session_id).first().date_created), "%m-%d")
        data_exercise[date] = [set_parser(ex), rep_exercise_parser(ex), weight_lifted_parser(ex)]

        if exercise.type in [1, 3]:
          total = set_parser(ex) * int(rep_exercise_parser(ex)) + (weight_lifted_parser(ex) / user.weight) * 100
        else:
          total = set_parser(ex) * rep_exercise_parser(ex) * weight_lifted_parser(ex)

        data_exercise[date].append(total)

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


def calendar_data_from_start(user_id):
    """Returns training sessions by date from the beginning"""
    session_dates = TrainingSession.query.filter_by(user_id=user_id).all()
    current_month, current_year, current_day = datetime.datetime.now().month, datetime.datetime.now().year, datetime.datetime.now().day

    first_session_date = session_dates[0].date_created

    for d in session_dates:
        if d.date_created < first_session_date:
            first_session_date = d.date_created

    start_date_temp = str(first_session_date).split(' ')[0]
    end_date = str(current_year) + '-' + str(current_month) + '-' + str(current_day)

    split_start_date = start_date_temp.split('-')
    start_date = split_start_date[0] + '-' + split_start_date[1] + '-01'

    start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    years_months = []
    calendar_data_list = []

    while start < end:
        years_months.append((start.timetuple()[1], start.timetuple()[0]))
        start += relativedelta(months=1)

    for tup in years_months:
        d = calendar_data(tup[0], tup[1])

        calendar_data_list.append((d, len(d), tup[0], tup[1]))

    return calendar_data_list


def training_session_by_id(session_id):
    training_session = TrainingSession.query.filter_by(id=session_id).first()
    exercises = training_session.exercises

    training_session_exercises = []

    for ex in exercises:
        training_session_exercises\
            .append([ex.ordinal_number, ex.exercise, ex.resistance, ex.sets, ex.reps])

    return training_session_exercises


# def get_tests():
#     return [t.to_json() for t in Tests.query.all()]


def insert_results(results, user_id, type):
    if type == 'anthropometry':
        anthropometry_test = AnthropometryTests(**results,
                                                user_id=user_id,
                                                date_done=datetime.datetime.utcnow(),
                                                test_name=type,
                                                test_category=type)
        db.session.add(anthropometry_test)
        db.session.commit()

    user = Users.query.get(user_id)

    for test in user.anthropometry_tests:
        print(test.to_json())

    return []


def get_test_history(user_id):
    tests_dict = {'anthropometry': [t.to_json() for t in AnthropometryTests.query.filter_by(user_id=user_id).all()],
                  'strength': None, 'mobility': None, 'endurance': None}

    return tests_dict
