from typing import Union

import requests
from ariadne import SchemaDirectiveVisitor
from graphql import default_field_resolver, GraphQLField, GraphQLObjectType, GraphQLInterfaceType

# Stepzen Rest directive configs:
#   endpoint(required) -> url
#   configuration(optional)
#   method(optional)
#   resultroot(optional)
#   setters(optional)
#   filter(optional)
#   headers(optional)
#   postbody (optional) -> payload
#   params [custom]
from main.engines.utils import replace_variables
from main.schemas.directive import RestDirectiveInputSchema


def _get_resolved_config(config: dict, variables: dict):
    url = config['url']
    request_method = config['method']
    headers = config.get('headers')
    params = config.get('params')
    payload = config.get('payload')

    # TODO: Refactor this so that it replaces vars in other configs as well
    # Replace $variable with its value in url, headers, params
    config['url'] = replace_variables(url, variables)
    if headers is not None:
        config['headers'] = {
            key: replace_variables(text=value, variables=variables)
            for key, value in headers.items()
        }
    if params is not None:
        config['params'] = {
            key: replace_variables(text=value, variables=variables)
            for key, value in params.items()
        }

    return config


class RestDirective(SchemaDirectiveVisitor):
    def visit_field_definition(
        self,
        field: GraphQLField,
        object_type: Union[GraphQLObjectType, GraphQLInterfaceType]
    ):
        config = RestDirectiveInputSchema().load(self.args)
        # print('config', config)

        original_resolver = field.resolve or default_field_resolver

        def resolve_rest(obj, info, **kwargs):
            resolved_config = _get_resolved_config(config, variables=kwargs)
            response = requests.request(
                resolved_config['method'],
                resolved_config['url'],
                params=resolved_config.get('params'),
                json=resolved_config.get('payload'),
                headers=resolved_config.get('headers'),
            )
            # print(params, headers)
            # print('response', response.json())
            return response.json()

        field.resolve = resolve_rest
        return field
