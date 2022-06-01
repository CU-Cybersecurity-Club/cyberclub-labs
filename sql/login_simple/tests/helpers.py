from app.session_helpers import logged_in, logged_in_as
from app.db import get_conn


def login_as(username, client):
    with client.session_transaction() as session:
        # Initialize session so that the user is logged in
        session['username'] = username

    # Sanity checks
    client.get("/")
    assert logged_in()
    assert logged_in_as() == username

# Note(klinvill): the database queries from app.db seem to fail when called directly unless we force a new connection. Given the current structure of app.db, that means duplicating them here.
def get_email(user):
    conn = get_conn()
    with conn.cursor() as cursor:
        cursor.execute("SELECT email FROM Users WHERE username=%s", (user,))
        email = cursor.fetchone()
    if email is not None:
        # MySQL returns the query results as a tuple
        email = email[0]
    return email


def get_grade(user, course):
    conn = get_conn()
    with conn.cursor() as cursor:
        cursor.execute("SELECT grade FROM Grades WHERE username=%s AND course=%s", (user, course))
        grade = cursor.fetchone()
    if grade is not None:
        # MySQL returns the query results as a tuple
        grade = grade[0]
    return grade
