import pytest
from app.db import init_db


@pytest.fixture()
def app():
    from app.main import app

    # Reset the database
    init_db()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
