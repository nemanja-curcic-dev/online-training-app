from . import main_blueprint
from ..models import Users


@main_blueprint.route('/')
def index():
    return "Hello"
