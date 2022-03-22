from flask import Flask, g, request
from flask_cors import CORS


def _init_app():
    return Flask(__name__)


def register_subpackages():
    import main.controllers  # noqa


app = _init_app()
CORS(app)
register_subpackages()


# Handle request events
@app.before_request
def handle_before_request():
    # Allow the pre-flight requests to get through
    if request.method == 'OPTIONS':
        return None
