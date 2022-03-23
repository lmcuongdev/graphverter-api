from flask import jsonify
from marshmallow import INCLUDE, Schema, post_dump


class BaseSchema(Schema):
    class Meta:
        unknown = INCLUDE

    @post_dump
    def remove_null_fields(self, data, **__):
        return {k: v for k, v in data.items() if v is not None}

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))
