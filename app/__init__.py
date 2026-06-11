import logging
import logging.handlers
import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class_name="config.Config", config_override=None):
    app = Flask(__name__)
    app.config.from_object(config_class_name)
    if config_override:
        app.config.update(config_override)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    _configure_logging(app)

    from app.routes import auth_bp, main_bp, task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(task_bp)

    os.makedirs(os.path.join(app.instance_path), exist_ok=True)
    with app.app_context():
        db.create_all()

    return app


def _configure_logging(app):
    log_level = logging.INFO
    log_format = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    stream_handler.setLevel(log_level)
    app.logger.addHandler(stream_handler)

    syslog_host = os.environ.get("SYSLOG_HOST", "localhost")
    syslog_port = int(os.environ.get("SYSLOG_PORT", 514))
    try:
        syslog_handler = logging.handlers.SysLogHandler(
            address=(syslog_host, syslog_port)
        )
        syslog_handler.setFormatter(log_format)
        syslog_handler.setLevel(log_level)
        app.logger.addHandler(syslog_handler)
    except Exception:
        app.logger.warning("Could not connect to syslog server at %s:%s", syslog_host, syslog_port)

    app.logger.setLevel(log_level)
