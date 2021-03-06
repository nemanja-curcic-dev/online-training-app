from flask import render_template, redirect, url_for, request
from . import main_blueprint
from flask_login import current_user
from ..models import Users


@main_blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        user = Users.query.filter_by(id=current_user.id).first()

        if user:
            if user.is_administrator:
                return redirect(url_for('admin_blueprint.admin'))
            else:
                return redirect(url_for('clients_blueprint.profile'))

    return render_template('main/index.html')


@main_blueprint.route('/')
def index():
    return render_template('main/index.html')


# views used by clients and admins

