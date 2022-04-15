from marshmallow import fields, pre_load

from main.schemas.base import BaseSchema


class EndpointSchema(BaseSchema):
    url = fields.String()
    method = fields.String()
    payload_json = fields.String()
    response_json = fields.String()
    suggested_schema_text = fields.String()


class SessionDataSchema(BaseSchema):
    endpoints = fields.Nested(EndpointSchema, many=True, dump_default=[])
    schema_text = fields.String(dump_default='')


class SessionSchema(BaseSchema):
    id = fields.Int()
    meta_data = fields.Nested(SessionDataSchema)


class UpdateSessionSchema(BaseSchema):
    endpoints = fields.Nested(
        EndpointSchema, many=True, required=False, allow_none=True
    )
    schema_text = fields.String(required=False, allow_none=True)

    @pre_load
    def remove_whitespaces(self, data, **__):
        if 'schema_text' in data:
            data['schema_text'] = data['schema_text'].strip()
        return data
