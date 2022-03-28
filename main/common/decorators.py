from functools import wraps

from flask import request
from marshmallow import Schema
from marshmallow import ValidationError as SchemaValidationError

from main.common.exceptions import Forbidden, NotFound, ValidationError
from main.engines.auth import get_user, parse_access_token
from main.engines.project import get_project


def validate_input(schema: Schema):
    """Validate input and append an `args` containing validated data"""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            request_data = request.get_json() or {}
            if request.method == 'GET':
                request_data = request.args.to_dict()

            try:
                valid_data = schema.load(request_data)
            except SchemaValidationError as e:
                raise ValidationError(error_data=e.messages)

            kwargs['args'] = valid_data
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def user_authenticated(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        # Decode the token to get the user_id stored in payload
        token = parse_access_token()

        # Get the authenticated user from database
        # Then pass it to the function being decorated
        kwargs['user'] = get_user(token)
        return fn(*args, **kwargs)

    return decorator


def validate_project(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        project = get_project(project_id=kwargs['project_id'])
        user = kwargs['user']

        if project is None:
            raise NotFound()

        if project.user_id != user.id:
            raise Forbidden(error_message='You are not allowed to view this project.')

        kwargs['project'] = project
        return fn(*args, **kwargs)

    return decorator
