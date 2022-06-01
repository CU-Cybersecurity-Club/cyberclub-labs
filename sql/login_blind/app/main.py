from flask import Flask, request, redirect, url_for, session, render_template
import secrets
from . import db
from .session_helpers import logged_in, logged_in_as
import os.path

# Path to the parent directory of this file
parent_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask("Blind SQL Injection", template_folder=os.path.join(parent_dir, "templates"))
app.secret_key = secrets.token_bytes()


@app.route("/", methods=['GET'])
def index():
    user=logged_in_as()
    if logged_in():
        grades, gpa = db.get_grades(user)
        db.set_last_page(user, request.user_agent.string, "index")
        return render_template('index.html.j2', user=user, grades=grades, gpa=gpa)
    else:
        return render_template('index.html.j2', user=user)

@app.route("/login", methods=['POST'])
def login():
    if not logged_in():
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = db.db_login(username, password)
        if user is not None:
            session['username'] = user
            last_page = db.get_last_page(user, request.user_agent.string)
            if last_page is None or last_page not in ["index", "profile"]:
                last_page = "index"
            return redirect(url_for(last_page))
    return redirect(url_for("index"))

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
            db.update_email(user, new_email)
            db.set_last_page(user, request.user_agent.string, "profile")
            return redirect(url_for("profile"))
        else:
            user = logged_in_as()
            email = db.get_email(user)
            db.set_last_page(user, request.user_agent.string, "profile")
            return render_template('profile.html.j2', user=user, email=email)
