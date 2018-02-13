from functools import wraps
from flask import abort
from flask_login import current_user
from blog.app.db_models import Permissions


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def deco_fun(*args, **kwargs):
            if not current_user.can(permission):
                abort(404)
            return f(*args, **kwargs)

        return deco_fun

    return decorator


def admin_required(f):
    return permission_required(Permissions.ADMINISTER)(f)
