from flask import render_template, abort
from . import clients_blueprint
from ..models import Users
from flask_login import login_required, current_user


@clients_blueprint.before_request
@login_required
def before_request():
    if current_user.is_authenticated:
        user = Users.query.filter_by(id=current_user.id).first()

        if user:
            user.seen()


@clients_blueprint.route('/clients/<id>')
@login_required
def profile(id):
    user = Users.query.filter_by(id=id).first()

    if user is None:
        abort(404)

    return render_template('clients/profile.html', user=user)