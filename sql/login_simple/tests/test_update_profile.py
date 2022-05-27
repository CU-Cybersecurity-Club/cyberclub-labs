from jinja2.filters import escape
from tests.helpers import login_as, get_email, get_grade


def test_normal_update(client):
    username = 'alice'
    new_email = 'asdhwert@gmail.com'
    with client:
        login_as(username, client)

        response = client.post("/profile", data={
            "email": new_email
        })
        assert response.status_code == 200
        response_body = response.get_data(as_text=True)
        query_prefix = "<div>Tried to update email using query: "
        query_suffix = "</div>"
        escaped_query = str(escape(f"UPDATE Users SET email='{new_email}' WHERE username='{username}'"))
        # Any attempt to change an email should show the SQL statement that was run
        expected_query = query_prefix + escaped_query + query_suffix
        assert expected_query in response_body

        # Make sure the email has been updated
        new_response = client.get("/profile")
        assert new_response.status_code == 200
        assert f"Email: {new_email}" in new_response.get_data(as_text=True)


def test_failed_update(client):
    username = 'alice'
    new_email = "uhoh@gmail.com'"
    with client:
        login_as(username, client)

        prev_email = get_email(username)
        # Sanity check
        assert prev_email is not None

        response = client.post("/profile", data={
            "email": new_email
        })
        assert response.status_code == 200
        response_body = response.get_data(as_text=True)
        query_prefix = "<div>Tried to update email using query: "
        query_suffix = "</div>"
        escaped_query = str(escape(f"UPDATE Users SET email='{new_email}' WHERE username='{username}'"))
        # Any attempt to change an email should show the SQL statement that was run
        expected_query = query_prefix + escaped_query + query_suffix
        assert expected_query in response_body

        # In this case the email should not have been updated:
        new_response = client.get("/profile")
        assert new_response.status_code == 200
        new_email = get_email(username)
        assert new_email == prev_email


def test_update_grade_through_profile(client):
    username = 'alice'
    new_email = "uhoh@gmail.com"
    course = "English"
    new_grade = "G"
    email_payload = f"{new_email}'; UPDATE Grades SET grade='{new_grade}' WHERE username='{username}' AND course='{course}'-- "
    with client:
        login_as(username, client)

        prev_email = get_email(username)
        prev_grade = get_grade(username, course)
        # Sanity checks
        assert prev_email is not None and prev_email != new_email
        assert prev_grade is not None and prev_grade != new_grade

        response = client.post("/profile", data={
            "email": email_payload
        })
        assert response.status_code == 200
        response_body = response.get_data(as_text=True)
        query_prefix = "<div>Tried to update email using query: "
        query_suffix = "</div>"
        escaped_query = str(escape(f"UPDATE Users SET email='{email_payload}' WHERE username='{username}'"))
        # Any attempt to change an email should show the SQL statement that was run
        expected_query = query_prefix + escaped_query + query_suffix
        assert expected_query in response_body

        # In this case both the email and grade should have been updated
        new_response = client.get("/profile")
        assert new_response.status_code == 200
        new_email_db = get_email(username)
        assert new_email_db == new_email
        new_grade_db = get_grade(username, course)
        assert new_grade_db == new_grade
