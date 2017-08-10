from . import auth_blueprint


@auth_blueprint.route('/')
def index():
    return "hello"
