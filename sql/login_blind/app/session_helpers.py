from flask import session

def logged_in():
    return 'username' in session

def logged_in_as():
    return session.get('username', None)
