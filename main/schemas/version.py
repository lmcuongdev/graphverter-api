from marshmallow import fields

from main.schemas.base import BaseSchema


class VersionSchema(BaseSchema):
    id = fields.Int()
    is_dirty = fields.Boolean()
