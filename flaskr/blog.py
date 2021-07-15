from flaskr.models import user
from flask import Blueprint
from flask import request
from flask import g
from flask.helpers import flash, url_for
from flask.templating import render_template
from sqlalchemy.orm.session import Session
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from sqlalchemy.orm import joinedload
from .auth import login_required
from .models import User, Post
from .db import get_db
bp = Blueprint("blog", __name__)

@bp.route("/")
def index():
    print(url_for("blog.update", id=[1]))
    posts = Post.query.options(joinedload('author'))
    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        error = None

        if title is None or len(title) <= 0:
            error = "Title is required"
        if body is None or len(body) <= 0:
            error = "Body is required"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            post = Post(title=title, body=body, author_id=g.user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/create.html")


def get_post(id, check_author=True):
    db = get_db()
    post = Post.query.join(User).add_columns(Post.id, Post.title, Post.body, Post.author_id, User.username).filter(Post.author_id == User.id).filter(Post.id == id).first()
    if post is None:
        abort(404, f'Post id {id} doesn\'t exsits')
    if check_author and post.author_id != g.user.id:
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
        if title is None or len(title) <= 0:
            error = "Title is required"
        if body is None or len(body) <= 0:
            error = "Body is required"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            post = Post.query.get(post['id'])
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    post = Post.query.get(id)    
    if post is None:
        abort(404, f"Post not found for id: {id}")
    
    db = get_db()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog.index"))




