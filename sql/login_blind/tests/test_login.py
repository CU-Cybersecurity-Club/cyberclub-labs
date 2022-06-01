import pytest
from app.session_helpers import logged_in, logged_in_as
from jinja2.filters import escape
from tests.helpers import login_as


def test_simple_failed_login(client):
    username = 'admin'
    password = 'test'
    with client:
        response = client.post("/login", data={
            "username": username,
            "password": password
        })
        # Should be redirected back to the home page
        assert response.status_code == 302
        assert not logged_in()


def test_alice_login(client):
    """Should be able to login as Alice using a well-known password."""
    username = 'alice'
    password = 'super_secret_password'
    with client:
        response = client.post("/login", data={
            "username": username,
            "password": password
        })
        # Should be redirected back to the home page
        assert response.status_code == 302
        assert logged_in()
        assert logged_in_as() == username


@pytest.mark.parametrize("target_user", ["admin", "alice", "charlie"])
def test_login_not_vulnerable_to_injection(client, target_user):
    username = f"{target_user}'-- "
    password = 'test'
    with client:
        response = client.post("/login", data={
            "username": username,
            "password": password
        })
        # Should be redirected back to the home page
        assert response.status_code == 302
        assert not logged_in()


def test_logout(client):
    username = 'admin'
    with client:
        login_as(username, client)

        response = client.get("/logout")
        # Should be redirected back to the home page
        assert response.status_code == 302
        assert not logged_in()
