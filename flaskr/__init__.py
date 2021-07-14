import os
from flask import Flask, redirect, url_for, has_request_context, request
from logging.config import dictConfig
from flask import logging, request_started, request_finished
from flask.logging import default_handler
from logging import Formatter, debug

# Adding signals for request
def log_request(sender, **extra):
    sender.logger.debug('Request context is set up')

def log_finished_request(sender, **extra):
    sender.logger.debug("Request context is finished")


class RequestFormatter(Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)


formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)

default_handler.setFormatter(formatter)

    
# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     }
# })

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    request_started.connect(log_request, app)
    request_finished.connect(log_finished_request, app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    
    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from flaskr import db    
    db.init_app(app)

    from flaskr import auth, blog

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(blog.bp)

    app.add_url_rule("/", endpoint="index")
    print("Flaskr application created")

    return app
