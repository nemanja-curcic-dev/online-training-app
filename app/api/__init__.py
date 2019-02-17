from flask.blueprints import Blueprint

api_blueprint = Blueprint('api_blueprint', __name__)

from . import views
