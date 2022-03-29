from marshmallow import fields, pre_load

from main.schemas.base import BaseSchema


class SessionSchema(BaseSchema):
    id = fields.Int()
    meta_data = fields.Raw()


class UpdateSessionSchema(BaseSchema):
    schema_text = fields.String(required=True)

    @pre_load
    def remove_whitespaces(self, data, **__):
        if 'schema_text' in data:
            data['schema_text'] = data['schema_text'].strip()
        return data
