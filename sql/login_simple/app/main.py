from flask import Flask, request, redirect, url_for, session, render_template
import secrets
from . import db
from .session_helpers import logged_in, logged_in_as
import os.path

# Path to the parent directory of this file
parent_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask("Simple Login", template_folder=os.path.join(parent_dir, "templates"))
app.secret_key = secrets.token_bytes()

@app.route("/", methods=['GET'])
def index():
    user=logged_in_as()
    if logged_in():
        grades, gpa = db.get_grades(user)
        return render_template('index.html.j2', user=user, grades=grades, gpa=gpa)
    else:
        return render_template('index.html.j2', user=user)

@app.route("/login", methods=['POST'])
def login():
    if not logged_in():
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user, query = db.db_login(username, password)
        if user is not None:
            session['username'] = user
        else:
            return render_template('login_status.html.j2', query=query)
    return redirect(url_for('index'))

@app.route("/logout", methods=['GET'])        
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/profile", methods=['GET', 'POST'])        
def profile():
    if not logged_in():
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            user = logged_in_as()
            new_email = request.form.get('email', '')
            query = db.update_email(user, new_email)
            return render_template('email_status.html.j2', query=query)
        else:
            user = logged_in_as()
            email = db.get_email(user)
            return render_template('profile.html.j2', user=user, email=email)
