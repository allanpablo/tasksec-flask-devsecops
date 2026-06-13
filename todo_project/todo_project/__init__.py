import logging
import os
from logging.handlers import SysLogHandler

from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app(config_override=None):
    instance_path = os.getenv("FLASK_INSTANCE_PATH")
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL", "sqlite:///" + os.path.join(app.instance_path, "site.db")
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        REMEMBER_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_SAMESITE="Lax",
    )
    if config_override:
        app.config.update(config_override)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "login"
    login_manager.login_message_category = "danger"

    configure_logging(app)
    register_security_headers(app)

    from . import routes

    routes.register_routes(app)

    with app.app_context():
        db.create_all()

    return app


def configure_logging(app):
    app.logger.setLevel(logging.INFO)
    if not any(isinstance(handler, SysLogHandler) for handler in app.logger.handlers):
        syslog_host = os.getenv("SYSLOG_HOST")
        syslog_port = int(os.getenv("SYSLOG_PORT", "514"))
        if syslog_host:
            handler = SysLogHandler(address=(syslog_host, syslog_port))
        else:
            handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        app.logger.addHandler(handler)


def register_security_headers(app):
    @app.after_request
    def add_security_headers(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "form-action 'self'; "
            "frame-src 'none'; "
            "child-src 'none'; "
            "worker-src 'none'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'"
        )
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["Cache-Control"] = "no-store"
        return response


def log_security_event(message, user="-", level="info"):
    from flask import current_app

    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr or "-")
    log_line = (
        f"SECURITY: {message} | user={user or '-'} | "
        f"ip={ip_address} | endpoint={request.path}"
    )
    getattr(current_app.logger, level, current_app.logger.info)(log_line)


app = create_app()
