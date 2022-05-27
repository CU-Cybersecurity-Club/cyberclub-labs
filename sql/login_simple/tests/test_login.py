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
        assert response.status_code == 200
        assert not logged_in()
        response_body = response.get_data(as_text=True)
        query_prefix = "<div>Failed to login using query: "
        query_suffix = "</div>"
        escaped_query = str(escape(f"SELECT username FROM Users WHERE username='{username}' and password='{password}'"))
        # A failed login should show the SQL statement that was run
        expected_query = query_prefix + escaped_query + query_suffix
        assert expected_query in response_body
        
@pytest.mark.parametrize("target_user", ["admin", "alice", "charlie"])
def test_successful_login(client, target_user):
    username = f"{target_user}'-- "
    password = 'test'
    with client:
        response = client.post("/login", data={
            "username": username,
            "password": password
        })
        # Should be redirected back to the home page
        assert response.status_code == 302
        assert logged_in()
        assert logged_in_as() == target_user


def test_logout(client):
    username = 'admin'
    with client:
        login_as(username, client)

        response = client.get("/logout")
        # Should be redirected back to the home page
        assert response.status_code == 302
        assert not logged_in()
