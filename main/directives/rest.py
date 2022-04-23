import re
from typing import Dict, List, Union

import requests
from ariadne import SchemaDirectiveVisitor

from graphql import GraphQLField, GraphQLInterfaceType, GraphQLObjectType

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
    headers = config.get('headers')
    params = config.get('params')

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


def get_nested_data(data: Union[Dict, List], path: List[str]):
    """Get nested data from path list"""
    regex = r'^\[\d+\]$'
    for key in path:
        if re.match(regex, key):
            # Take the index of the list if key is like "[0]", "[1]",...
            index = int(key[1:-1])
            data = data[index]
            continue
        if isinstance(data, list):
            # For each instance, get the specified key
            # In case the instance is list, convert the key to get the index
            data = list(
                map(lambda _: _.get(key) if isinstance(_, dict) else _[int(key)], data)
            )
            continue
        # Assume type is dict
        data = data[key]
    return data


class RestDirective(SchemaDirectiveVisitor):
    def visit_field_definition(
        self,
        field: GraphQLField,
        object_type: Union[GraphQLObjectType, GraphQLInterfaceType],
    ):
        config = RestDirectiveInputSchema().load(self.args)
        # print('config', config)

        def resolve_rest(obj, info, **kwargs):
            if kwargs.get('_payload'):
                # To use @rest with payload, user must provide _payload as argument
                config['payload'] = kwargs.pop('_payload')

            resolved_config = _get_resolved_config(config, variables=kwargs)
            response = requests.request(
                resolved_config['method'],
                resolved_config['url'],
                params=resolved_config.get('params'),
                json=resolved_config.get('payload'),
                headers=resolved_config.get('headers'),
            )

            # Get nested data from `result_root` option and use it as result
            result = get_nested_data(
                data=response.json(),
                path=resolved_config['result_root'],
            )

            # Resolve `setters` if it's set
            if resolved_config['setters']:
                if isinstance(result, list):
                    # Iterate each item and set the setters
                    for item in result:
                        for setter in resolved_config['setters']:
                            item[setter['field']] = get_nested_data(
                                item, path=setter['path']
                            )
                else:
                    # Assume this is dict, set the setters directly
                    for setter in resolved_config['setters']:
                        result[setter['field']] = get_nested_data(
                            result, path=setter['path']
                        )

            return result

        field.resolve = resolve_rest
        return field
