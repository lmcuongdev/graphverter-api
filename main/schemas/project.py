from marshmallow import fields, pre_load, validate

from main.engines.utils import trim_data
from main.schemas.base import BaseSchema, PaginationSchema
from main.schemas.session import SessionSchema

API_PATH_REGEX = r'^[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?$'


class CreateProjectSchema(BaseSchema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=64))
    api_path = fields.String(
        required=True,
        validate=[
            validate.Length(min=1, max=50),
            validate.Regexp(
                regex=API_PATH_REGEX,
                error='Path can only consist of lowercase letters, numbers, and dashes. '
                'But it can\'t start nor end with dashes',
            ),
        ],
    )

    @pre_load
    def remove_white_spaces(self, data: dict, **_):
        return trim_data(data)


class ProjectBaseSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    api_path = fields.String()
    is_deployed = fields.Boolean()
    updated = fields.DateTime()


class ProjectsSchema(PaginationSchema):
    items = fields.Nested(ProjectBaseSchema, many=True)


class ProjectDetailSchema(ProjectBaseSchema):
    session = fields.Nested(SessionSchema)
