from flask import render_template, abort, flash, g
from . import clients_blueprint
from ..models import Users
from flask_login import login_required, current_user
from app import db
from .helper_functions import is_client


@clients_blueprint.before_request
@login_required
@is_client
def before_request():
    if current_user.is_authenticated:
        user = Users.query.filter_by(id=current_user.id).first()

        if user:
            user.seen()

        if user.has_new_training:
            flash('You have a new training! You can check it out in training category!')
            user.has_new_training = False
            db.session.add(user)
            db.session.commit()


@clients_blueprint.route('/clients')
@login_required
@is_client
def profile():
    user = Users.query.filter_by(id=current_user.id).first()

    if user is None:
        abort(404)

    return render_template('clients/profile.html', user=user)