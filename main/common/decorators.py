from functools import wraps

from flask import request
from marshmallow import Schema
from marshmallow import ValidationError as SchemaValidationError

from main.common.exceptions import ValidationError


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
