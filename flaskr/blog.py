from flask import Blueprint
from flask import request
from flask import g
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from .db import get_db
from .auth import login_required

bp = Blueprint("blog", __name__)

@bp.route("/")
def index():
    print(url_for("blog.update", id=[1]))
    db = get_db()
    posts = db.execute(  "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC").fetchall()
    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        error = None

        if title is None:
            error = "Title is required"
        if body is None:
            error = "Body is required"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user['id']),
            )
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/create.html")


def get_post(id, check_author=True):
    post = (get_db().execute("select p.id, title, body, created, author_id, username"
                        " FROM post p JOIN user u on p.author_id = u.id"
                        " where p.id = ?", (id,),)
                        .fetchone()
            )
    if post is None:
        abort(404, f'Post id {id} doesn\'t exsits')
    if check_author and post['author_id'] != g.user["id"]:
        abort(403, "Access denied to this post")
    
    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        error = None
        if title is None:
            error = "Title is required"
        if body is None:
            error = "Body is required"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? where id = ?",
                (title, body, post['id']),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    post = get_post(id)
    
    if post is None:
        abort(404, f"Post not found for id: {id}")
    
    db = get_db()
    db.execute("DELETE from post where id = ? ", (id,),)
    db.commit()

    return redirect(url_for("blog.index"))




