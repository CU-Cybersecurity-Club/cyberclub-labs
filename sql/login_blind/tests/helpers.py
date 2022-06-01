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


def logout(client):
    with client.session_transaction() as session:
        del session['username']

    # Sanity checks
    client.get("/")
    assert not logged_in()


# Note(klinvill): the database queries from app.db seem to fail when called directly unless we force a new connection. Given the current structure of app.db, that means duplicating them here.
def get_email(user):
    with get_conn(force_new=True) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM Users WHERE username=%s", (user,))
            email = cursor.fetchone()
    if email is not None:
        # MySQL returns the query results as a tuple
        email = email[0]
    return email


def get_grade(user, course):
    with get_conn(force_new=True) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT grade FROM Grades WHERE username=%s AND course=%s", (user, course))
            grade = cursor.fetchone()
    if grade is not None:
        # MySQL returns the query results as a tuple
        grade = grade[0]
    return grade


def get_last_page(user, user_agent):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            query = "SELECT last_page FROM LastPage WHERE username=%s and user_agent=%s"
            
            cursor.execute(query, (user, user_agent))
            last_page = cursor.fetchone()

    if last_page is not None:
        # MySQL returns the query results as a tuple
        last_page = last_page[0]
    return last_page


def set_last_page(user, user_agent, page):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            if get_last_page(user, user_agent) is not None:
                query = "UPDATE LastPage SET last_page=%s WHERE username=%s AND user_agent=%s"
            else:
                query = "INSERT INTO LastPage (last_page, username, user_agent) VALUES (%s, %s, %s)"
            cursor.execute(query, (page, user, user_agent))
        conn.commit()
