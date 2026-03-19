from __future__ import annotations

from functools import wraps

from flask import abort
from flask_login import current_user


def role_required(role: str):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if getattr(current_user, "role", None) != role:
                abort(403)
            return func(*args, **kwargs)

        return wrapped

    return decorator
