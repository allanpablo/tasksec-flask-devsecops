import logging
from functools import wraps

from flask import current_app, request

logger = logging.getLogger(__name__)


def log_security_event(event: str, user: str = "anonymous", level: str = "warning"):
    log_msg = f"SECURITY: {event} | user={user} | ip={request.remote_addr} | endpoint={request.path}"
    getattr(logger, level, logger.warning)(log_msg)
    if current_app:
        getattr(current_app.logger, level, current_app.logger.warning)(log_msg)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import abort
        from flask_login import current_user

        if not current_user.is_authenticated:
            abort(401)
        if current_user.username != "admin":
            abort(403)
        return f(*args, **kwargs)

    return decorated_function
