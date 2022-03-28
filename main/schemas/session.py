from marshmallow import fields

from main.schemas.base import BaseSchema


class SessionSchema(BaseSchema):
    id = fields.Int()
    meta_data = fields.Raw()
