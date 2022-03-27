from marshmallow import fields

from main.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    id = fields.Int()
    username = fields.String()
