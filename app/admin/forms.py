from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class AddExercise(FlaskForm):
    exercise_name = StringField('Exercise name', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[(1, 'compound'), (2, 'auxiliary'), (3, 'isolated')])
    direction = SelectField('Direction', choices=[('push', 'push'), ('pull', 'pull')])
    type = SelectField('Type', choices=[(1, 'bodyweight'), (2, 'weight'), (3, 'complex')])