import mysql.connector
import os
import secrets
from flask import g, has_app_context
from time import sleep


def get_db_pass():
    db_pass = os.environ["DB_USER_PASSWORD"]
    return db_pass


def get_conn(force_new=False) -> mysql.connector.MySQLConnection:
    if has_app_context() and 'db' in g and not force_new:
        # If we're running from flask, try to reuse the connection object
        print("Returned saved connection", flush=True)
        return g.db
    else:
        db_pass = get_db_pass()
        # It seems to take a long time for the mysql container to startup
        attempts = 30
        for attempt in range(attempts):
            try:
                conn = mysql.connector.connect(user='webapp', password=db_pass, database='webapp', host='db')
                if has_app_context():
                    g.db = conn
                break
            except (mysql.connector.errors.DatabaseError, mysql.connector.errors.InterfaceError) as e:
                if attempt == attempts - 1:
                    raise e
                else:
                    sleep(2)
        return conn


def db_login(user, password):
    conn = get_conn()
    with conn.cursor() as cursor:
        query = f"SELECT username FROM Users WHERE username='{user}' and password='{password}'"
        try:
            cursor.execute(query)
            user = cursor.fetchone()
        except mysql.connector.errors.Error as e:
            print(f"Error while executing login query: {e}")
            user = None
    
    if user is not None:
        # MySQL returns the query results as a tuple
        user = user[0]

    return user, query


def grade_points(letter_grade):
    if letter_grade == "A":
        return 4
    elif letter_grade == "B":
        return 3
    elif letter_grade == "C":
        return 2
    elif letter_grade == "D":
        return 1
    else:
        return 0


def get_grades(user):
    conn = get_conn()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Grades WHERE username=%s", (user,))
        grades = cursor.fetchall()
    
    letter_grades = [grade[2] for grade in grades]
    if len(grades) == 0:
        gpa = "N/A"
    else:
        gpa = sum([grade_points(l) for l in letter_grades]) / len(grades)
    return grades, gpa


def get_email(user):
    conn = get_conn()
    with conn.cursor() as cursor:
        cursor.execute("SELECT email FROM Users WHERE username=%s", (user,))
        email = cursor.fetchone()
    if email is not None:
        # MySQL returns the query results as a tuple
        email = email[0]
    return email


def update_email(user, email):
    conn = get_conn()
    with conn.cursor() as cursor:
        query = f"UPDATE Users SET email='{email}' WHERE username='{user}'"
        try:
            for result in cursor.execute(query, multi=True):
                changed = result.rowcount
        except mysql.connector.errors.Error as e:
            print(f"Error while executing email update query: {e}")
    try:
        conn.commit()
    except mysql.connector.errors.Error as e:
            print(f"Error while executing email update query: {e}")
    return query


def insert_users():
    users = [
        "admin",
        "alice",
        "bob",
        "charlie"
    ]

    grades = [
        {"user": "alice", "course": "Biology", "grade": "B"},
        {"user": "alice", "course": "Computer Science", "grade": "A"},
        {"user": "alice", "course": "English", "grade": "C"},
        {"user": "bob", "course": "Biology", "grade": "B"},
        {"user": "bob", "course": "Computer Science", "grade": "B"},
        {"user": "bob", "course": "English", "grade": "A"},
        {"user": "charlie", "course": "Biology", "grade": "A"},
        {"user": "charlie", "course": "Computer Science", "grade": "C"},
        {"user": "charlie", "course": "English", "grade": "A"},
    ]

    user_table = "Users"
    grades_table = "Grades"

    conn = get_conn()
    with conn.cursor() as cursor:
        # First clear existing rows
        cursor.execute(f"TRUNCATE TABLE {user_table}")
        cursor.execute(f"TRUNCATE TABLE {grades_table}")

        # Then add new rows
        for user in users:
            cursor.execute(f"INSERT INTO {user_table} (username, password, email) VALUES (%s, %s, %s)", (user, secrets.token_urlsafe(), f"{user}@school.edu"))

        for entry in grades:    
            cursor.execute(f"INSERT INTO {grades_table} (username, course, grade) VALUES (%s, %s, %s)", (entry["user"], entry["course"], entry["grade"]))

    conn.commit()


def init_db():
    conn = get_conn()
    with conn.cursor() as cursor:
        # Drop old tables
        cursor.execute("DROP TABLE IF EXISTS Users")
        cursor.execute("DROP TABLE IF EXISTS Grades")

        # Create new tables
        cursor.execute("""
            CREATE TABLE Users (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE Grades (
                username TEXT NOT NULL,
                course TEXT NOT NULL,
                grade TEXT NOT NULL
            )
        """)

    # And then populate them
    insert_users()


if __name__ == "__main__":
    # Initialize the database if we run this file directly
    init_db()
