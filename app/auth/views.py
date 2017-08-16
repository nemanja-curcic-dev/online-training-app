from flask import render_template, request, flash, redirect, url_for
from . import auth_blueprint
from .forms import LogIn, Register, ForgotPassword, ResetPassword
from ..models import Users
from app import db
from ..send_email import send_mail
from flask_login import login_user, logout_user, login_required, current_user


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LogIn(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data) and user.confirmed:
            login_user(user=user, remember=form.remember_me.data)
            flash('You logged in successfully.')

            if user.is_administrator:
                return redirect(url_for('admin_blueprint.admin', id=user.id))
            else:
                return redirect(url_for('clients_blueprint.profile', id=user.id))

    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = Register(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        user = Users(first_name=form.first_name.data, last_name=form.last_name.data,
                     email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        token = user.generate_token()
        send_mail(sender='Personal training diary team', subject='Account confirmation',
                  to=user.email, template='email/confirm_account', token=token, user=user)

        flash('You have been successfully registered. '
              'Before you can log in you must confirm your '
              'account by clicking on a link that has '
              'been sent to the email address you provided.')
        return redirect(url_for('main_blueprint.index'))

    return render_template('auth/register.html', form=form)


@auth_blueprint.route('/confirm/<token>')
def confirm(token):
    if Users.check_token(token):
        flash('You have confirmed your account successfully! You can now log in!')
        return redirect(url_for('auth_blueprint.login'))

    flash('Sorry, your confirmation link was invalid or expired!')
    return redirect(url_for('main_blueprint.index'))


@auth_blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPassword(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if user:
            token = user.generate_token()
            send_mail(sender='Personal training diary',
                      subject='Password reset',
                      to=form.email.data,
                      template='email/password_reset', token=token, user=user)
            flash('Message with link for resetting your password has been sent to the email address you provided.')
            return redirect(url_for('main_blueprint.index'))
        else:
            flash('Email you provided doesn\'t exist in database.')
            return redirect(url_for('main_blueprint.index'))

    return render_template('auth/forgot_password.html', form=form)


@auth_blueprint.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main_blueprint.index'))

    form = ResetPassword(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        user = Users.from_token(token)

        if user:
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()

            flash('You changed your password successfully.')
            return redirect(url_for('auth_blueprint.login'))
        else:
            return redirect(url_for('main_blueprint.index'))

    return render_template('auth/password_reset.html', form=form, token=token)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out successfully.')
    return redirect(url_for('main_blueprint.index'))
