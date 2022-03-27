from flask import jsonify
from marshmallow import ValidationError

from main import app, db
from main.common.decorators import validate_input
from main.common.exceptions import InvalidCredentials
from main.engines.auth import create_access_token, get_login_user, validate_username
from main.engines.user import create_user
from main.schemas.auth import LoginSchema, RegisterSchema


@app.route('/auth/register', methods=['POST'])
@validate_input(RegisterSchema())
def register(args, **__):
    validate_username(args['username'])

    user = create_user(**args)
    db.session.commit()

    return jsonify({'access_token': create_access_token(user)})


@app.route('/auth/login', methods=['POST'])
@validate_input(LoginSchema())
def login(args, **__):
    # If the username or password doesn't match our database design,
    # then we don't need to query the database, instead return the
    # unauthorized response right away
    try:
        args = RegisterSchema().load(args)
    except ValidationError:
        raise InvalidCredentials()

    username, password = args['username'], args['password']
    user = get_login_user(username, password)

    return jsonify({'access_token': create_access_token(user)})
