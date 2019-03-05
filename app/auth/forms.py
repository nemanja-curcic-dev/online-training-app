from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from ..models import Users


class Register(FlaskForm):
    first_name = StringField('First name',
                             validators=[DataRequired(message='First name is required.'),
                             Length(min=2, max=30, message='First name must be between 2 and 30 characters long.')])
    last_name = StringField('Last name',
                            validators=[DataRequired(message='Last name is required.'),
                            Length(min=2, max=30, message='Last name must be between 2 and 30 characters long.')])
    email = EmailField('Email', validators=[DataRequired(
        message='Email is required.'
    ), Email(), Length(min=8, max=50, message='Length of email must be between 8 and 50 characters long.')])
    password = PasswordField('Password', validators=[DataRequired(
        message='Password is required.'
    ), Length(min=8, max=30,
              message='Password must be between 8 and 30 characters long.')])
    retype_password = PasswordField('Retype password', validators=[DataRequired(
        message='It\'s required to repeat password.'
    ), Length(min=8, max=30, message='Password must be between 8 and 30 characters long.'),
                                    EqualTo('password', message='Passwords must match!')])

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists in database.')


class LogIn(FlaskForm):
    email = StringField('Email', validators=[DataRequired(
        message='Email is required.'
    ), Email(), Length(min=8, max=50, message='Length of email must be between 8 and 50 characters long.')])
    password = PasswordField('Password', validators=[DataRequired(
        'Password is required.'
    ), Length(min=8, max=30, message='Password must be between 8 and 30 characters long.')])
    remember_me = BooleanField('Remember me')


class ForgotPassword(FlaskForm):
    email = StringField('Email', validators=[DataRequired(
        message='Email is required.'
    ), Email(), Length(min=8, max=50, message='Length of email must be between 8 and 50 characters long.')])


class ResetPassword(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=30),
                                         EqualTo('retype_password', message='Passwords must match!')])
    retype_password = PasswordField('Retype password', validators=[DataRequired(), Length(min=8, max=30)])
