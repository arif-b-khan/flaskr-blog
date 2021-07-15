import sqlite3
import click
import pdb

from sqlite3.dbapi2 import PARSE_DECLTYPES
from flask import current_app, g
from werkzeug.security import generate_password_hash
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from . import orm

def get_db():
    print(f"DATABASE: getting db {g is None}")    
    return orm


def close_db(e=None):
    print("Closing db instance")
    db = g.pop('db', None)
    if db is not None:
        db.session.close()
    

def init_db():
    print("Initializing database")
    print(current_app.config["DATABASE"])
    db = get_db()
    from .models import Employee, User, Post
    print("Creating tables")
    pwd = generate_password_hash("12345")
    arif = User.query.filter_by(username='arif').first()
    if arif is None:
        arif = User(username="arif", password=pwd)
        Post(title="test", body="test body", author=arif)
        db.session.add(arif)
        db.session.commit()
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialize database")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
