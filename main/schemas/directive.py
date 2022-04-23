from marshmallow import fields, post_load, pre_load, validate

from main.enums import RestMethod
from main.libs.misc import parse_path
from main.schemas.base import BaseSchema

SPACE_NOT_ALLOWED_ERROR = 'String must not contains any space.'


class NameValuePairSchema(BaseSchema):
    name = fields.String(required=True)
    value = fields.String(required=True)


class SetterInputSchema(BaseSchema):
    field = fields.String(
        required=True,
        validate=validate.ContainsNoneOf(' ', error=SPACE_NOT_ALLOWED_ERROR),
    )
    path = fields.String(
        required=True,
        validate=validate.ContainsNoneOf(' ', error=SPACE_NOT_ALLOWED_ERROR),
    )


class RestDirectiveInputSchema(BaseSchema):
    # TODO Med: Validate valid url, remove query string
    url = fields.String(required=True)
    method = fields.String(
        required=False,
        validate=validate.OneOf(RestMethod.get_list()),
        load_default=RestMethod.GET,
    )
    headers = fields.Nested(NameValuePairSchema, required=False, many=True)
    params = fields.Nested(NameValuePairSchema, required=False, many=True)
    setters = fields.Nested(
        SetterInputSchema, required=False, many=True, load_default=[]
    )
    resultRoot = fields.String(
        required=False,
        allow_none=True,
        load_default=None,
        validate=validate.ContainsNoneOf(' ', error=SPACE_NOT_ALLOWED_ERROR),
    )

    @pre_load
    def pre_process_data(self, data: dict, **_):
        if isinstance(data.get('method'), str):
            data['method'] = data['method'].lower()
        data['result_root'] = data.get('resultRoot')
        return data

    @post_load
    def reformat_data(self, data, **_):
        # Convert payload, headers, params to dict
        for field in ['headers', 'params']:
            if field in data:
                # Aware that it might have duplicated keys
                data[field] = {pair['name']: pair['value'] for pair in data[field]}

        if data.get('resultRoot') is not None:
            data['result_root'] = parse_path(data['resultRoot'])
        else:
            data['result_root'] = []

        for setter in data.get('setters', []):
            setter['path'] = parse_path(setter['path'])

        return data
