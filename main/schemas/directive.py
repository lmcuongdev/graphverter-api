from marshmallow import (
    ValidationError,
    fields,
    post_load,
    pre_load,
    validate,
    validates_schema,
)

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


class ArgumentInputSchema(BaseSchema):
    name = fields.String(required=True)
    field = fields.String(required=False)
    argument = fields.String(required=False)

    @validates_schema
    def validate_schema(self, data, *_, **__):
        if 'field' in data and 'argument' in data:
            raise ValidationError(
                message='Must provide only one of the two field `field` or `argument`.'
            )
        if 'field' not in data and 'argument' not in data:
            raise ValidationError(message='Missing field `field` or `argument`.')


class CombineDirectiveInputSchema(BaseSchema):
    query = fields.String(required=True)
    arguments = fields.Nested(ArgumentInputSchema, many=True, required=False)
