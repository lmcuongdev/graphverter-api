from marshmallow import INCLUDE, Schema, fields


class BaseSchema(Schema):
    class Meta:
        unknown = INCLUDE
