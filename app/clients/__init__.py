from flask.blueprints import Blueprint

clients_blueprint = Blueprint('clients_blueprint', __name__)

from . import views