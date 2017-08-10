from flask import render_template
from . import admin_blueprint
from ..models import Users


@admin_blueprint.route('/admin')
def admin():
    return render_template('admin/index.html')
