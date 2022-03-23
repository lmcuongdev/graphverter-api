from importlib import import_module

from flask import Flask, g, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from main.common.error_handlers import register_error_handlers


def _init_app():
    return Flask(__name__)


def _init_db(app):
    return SQLAlchemy(app)


def register_subpackages():
    from main import models

    for m in models.__all__:
        import_module('main.models.' + m)

    import main.controllers  # noqa


app = _init_app()
db = _init_db(app)
CORS(app)
register_subpackages()
register_error_handlers(app)


# Handle request events
@app.before_request
def handle_before_request():
    # Allow the pre-flight requests to get through
    if request.method == 'OPTIONS':
        return None
