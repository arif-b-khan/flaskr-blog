import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request, 
    session, 
    url_for
)
from werkzeug import wrappers
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from .models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@auth_bp.route('/register', methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'
        elif (
            User.query.filter_by(username = username).first()
            is not None
        ):
            error = f'Username: {username} already exists'

        if error is None:
            user = User(username=username, password=generate_password_hash(password))
            db.sesssion.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        
        flash(error)

    if g.user.id is None: 
        return render_template("auth/register.html")
    else: 
        return redirect(url_for("index"))


@auth_bp.route('/login', methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = User.query.filter_by(username=username).first()
        error = None
        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user.password, password):
            error = "Incorrect password"
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for("index"))
        
        flash(error)

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))