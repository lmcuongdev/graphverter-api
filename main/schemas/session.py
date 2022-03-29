from marshmallow import fields, pre_load

from main.engines.utils import trim_data
from main.schemas.base import BaseSchema


class SessionSchema(BaseSchema):
    id = fields.Int()
    meta_data = fields.Raw()


class UpdateSessionSchema(BaseSchema):
    schema_text = fields.String(required=True)

    @pre_load
    def remove_whitespaces(self, data, **__):
        return trim_data(data)
