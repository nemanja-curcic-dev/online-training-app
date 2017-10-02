from ..models import Users
from functools import wraps
from flask_login import current_user
from flask import abort


def is_client(original_function):
    """Check if user is a client, if is, returns original function, else return 403 error(forbidden)"""
    @wraps(original_function)
    def wrapper(*args, **kwargs):
        user = Users.query.filter_by(id=current_user.id).first()

        if user:
            if not user.is_administrator:
                return original_function(*args, **kwargs)
            else:
                return abort(403)
        else:
            return abort(403)
    return wrapper
