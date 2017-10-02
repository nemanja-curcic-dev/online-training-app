from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import DataRequired


class AddExercise(FlaskForm):
    exercise_name = StringField('Exercise name', validators=[DataRequired()])
    utility = SelectField('Utility', choices=[(1, 'basic'), (2, 'auxiliary')])
    mechanics = SelectField('Priority', choices=[(1, 'compound'), (2, 'isolated')])
    direction = SelectField('Direction', choices=[
        ('push', 'push'), ('pull', 'pull'), ('iso', 'isometric'), ('com', 'complex')])
    type = SelectField('Type', choices=[(1, 'bodyweight'), (2, 'weight'), (3, 'complex')])
    equipment = SelectField('Equipment', choices=[], coerce=int)
    description = TextAreaField('Description')
    instructions = TextAreaField('Instructions')


class CheckBoxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CreateTraining(FlaskForm):
    clients = SelectField('Clients', choices=[], coerce=int)
    training_goal = StringField('Training goal', validators=[DataRequired()])
    muscle_groups_checkbox = CheckBoxField('Label', choices=[], coerce=int)
    training = TextAreaField('Training')
    annotations = TextAreaField('Annotations')


class ClientsProfiles(FlaskForm):
    clients_profiles = SelectField('Clients', choices=[], coerce=int)
