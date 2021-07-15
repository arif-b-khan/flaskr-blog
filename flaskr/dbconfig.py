from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g
from flask.cli import with_appcontext


db = get_orm()

