import json

from marshmallow import fields, validate, pre_load, post_load

from main.schemas.base import BaseSchema


class NameValuePairSchema(BaseSchema):
    name = fields.String(required=False)
    value = fields.String(required=False)


class RestDirectiveInputSchema(BaseSchema):
    # TODO Med: Validate valid url, remove query string
    url = fields.String(required=True)
    method = fields.String(
        required=False,
        validate=validate.OneOf(['get', 'post', 'put', 'delete', 'patch']),
        load_default='get',
    )
    headers = fields.Nested(NameValuePairSchema, required=False, many=True)
    params = fields.Nested(NameValuePairSchema, required=False, many=True)

    @pre_load
    def lowercase_method(self, data: dict, **_):
        if isinstance(data.get('method'), str):
            data['method'] = data['method'].lower()
        return data

    @post_load
    def reformat_data(self, data, **_):
        # Convert payload, headers, params to dict
        for field in ['headers', 'params']:
            if field in data:
                # Aware that it might have duplicated keys
                data[field] = {
                    pair['name']: pair['value'] for pair in data[field]
                }

        return data
