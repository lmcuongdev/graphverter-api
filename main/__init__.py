from importlib import import_module

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from main.common.error_handlers import register_error_handlers
from main.config import config
from main.libs.memcache_client import MemcacheClient


def _init_app():
    app = Flask(__name__)
    app.config.from_object(config)
    return app


def _init_db(app):
    return SQLAlchemy(app)


def _init_memcache():
    return MemcacheClient(
        config.MEMCACHED_SERVERS,
        prefix_key=config.MEMCACHED_KEY_PREFIX,
    )


def register_subpackages():
    from main import models

    for m in models.__all__:
        import_module('main.models.' + m)

    import main.controllers  # noqa


app = _init_app()
db = _init_db(app)
memcache_client = _init_memcache()
CORS(app)
register_subpackages()
register_error_handlers(app)


# Handle request events
@app.before_request
def handle_before_request():
    # Allow the pre-flight requests to get through
    if request.method == 'OPTIONS':
        return None
