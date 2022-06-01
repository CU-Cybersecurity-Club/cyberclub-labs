import pytest
from app.session_helpers import logged_in
from tests.helpers import login_as


@pytest.mark.parametrize("route", [
    "/profile",
    "/logout"
])
def test_unauthorized(client, route):
    with client:
        response = client.get(route)
        # Should be redirected back to the home page to login
        assert response.status_code == 302
        assert not logged_in()


@pytest.mark.parametrize("route", [
    "/",
    "/profile",
])
def test_header(client, route):
    """Header should be present that allows navigation to other pages, logging out, and displays username"""
    expected_hrefs = ["/", "/profile", "/logout"]
    username = 'alice'
    with client:
        login_as(username, client)

        response = client.get(route, follow_redirects=True)

        assert response.status_code == 200
        response_body = response.get_data(as_text=True)
        for href in expected_hrefs:
            assert f'href="{href}"' in response_body
        assert username in response_body


def test_index_allows_login(client):
    with client:
        response = client.get("/")
        assert response.status_code == 200
        assert not logged_in()
        assert f'action="/login"' in response.get_data(as_text=True)


def test_profile_allows_update(client):
    with client:
        login_as("alice", client)

        response = client.get("/profile")
        assert response.status_code == 200
        assert f'<form method="POST">' in response.get_data(as_text=True)
