from tests.helpers import login_as, get_email, get_grade


def test_normal_update(client):
    username = 'alice'
    new_email = 'asdhwert@gmail.com'
    with client:
        login_as(username, client)

        response = client.post("/profile", data={
            "email": new_email
        })
        # Should be redirected back to profile page
        assert response.status_code == 302

        # Make sure the email has been updated
        new_response = client.get("/profile")
        assert new_response.status_code == 200
        assert f"Email: {new_email}" in new_response.get_data(as_text=True)


def test_update_email_not_vulnerable_to_injection(client):
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
        # Should be redirected back to profile page
        assert response.status_code == 302

        # In this case neither the email nor the grade should have been updated
        new_response = client.get("/profile")
        assert new_response.status_code == 200
        new_email_db = get_email(username)
        # Since we use prepared statements and don't check emails for validity, the whole email payload should be stored as the new email
        assert new_email_db == email_payload
        new_grade_db = get_grade(username, course)
        assert new_grade_db == prev_grade
