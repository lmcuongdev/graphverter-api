from marshmallow import fields

from .base import BaseSchema


class ErrorSchema(BaseSchema):
    error_message = fields.String(required=True)
    error_data = fields.Dict(allow_none=False)
