import os
import tempfile

import pytest
from app import create_app, db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(
        config_override={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            "WTF_CSRF_ENABLED": False,
            "SECRET_KEY": "test-secret",
        }
    )
    with app.app_context():
        db.create_all()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    class AuthActions:
        def __init__(self, client):
            self._client = client

        def register(
            self, username="testuser", email="test@example.com", password="secret123"
        ):
            return self._client.post(
                "/auth/register",
                data={
                    "username": username,
                    "email": email,
                    "password": password,
                    "password2": password,
                },
            )

        def login(self, username="testuser", password="secret123"):
            return self._client.post(
                "/auth/login",
                data={"username": username, "password": password},
            )

        def logout(self):
            return self._client.get("/auth/logout")

    return AuthActions(client)
