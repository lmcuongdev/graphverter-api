from typing import Union

from ariadne import SchemaDirectiveVisitor
from graphql import default_field_resolver, GraphQLField, GraphQLObjectType, GraphQLInterfaceType


class AnonymizeDirective(SchemaDirectiveVisitor):
    def visit_field_definition(
        self,
        field: GraphQLField,
        object_type: Union[GraphQLObjectType, GraphQLInterfaceType]
    ):
        anon_type = self.args.get('type')
        original_resolver = field.resolve or default_field_resolver

        def resolve_anonymize(obj, info, **kwargs):
            print('resolve_anonymize', obj, info, kwargs)
            result = original_resolver(obj, info, **kwargs)
            if result is None:
                return None

            if anon_type == 'email':
                return 'anon_email@got-it.ai'
            elif anon_type == 'name':
                return 'John Doe'

            return result

        field.resolve = resolve_anonymize
        return field
