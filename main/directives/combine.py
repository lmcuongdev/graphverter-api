import json
from typing import List, Union

from ariadne import SchemaDirectiveVisitor, graphql_sync

from graphql import (
    FieldNode,
    GraphQLField,
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLResolveInfo,
)
from main import app
from main.libs.log import ServiceLogger
from main.schemas.directive import CombineDirectiveInputSchema

logger = ServiceLogger(__name__)


def _build_query(query_name: str, variables: dict, requested_data: str) -> dict:
    # Turn variables into query arguments
    # e.g variables={'team_id': 1, apiKey='secret'}
    # then query_arguments=`(team_id: 1, apiKey: "secret")`
    query_arguments = (
        '({})'.format(
            ', '.join([f'{key}: {json.dumps(val)}' for key, val in variables.items()])
        )
        if variables
        else ''
    )
    query = f'{{ {query_name}{query_arguments} {requested_data} }}'

    return {
        'query': query,
    }


def _generate_variables(
    obj: dict, query_args: dict, directive_args: List[dict]
) -> dict:
    """
    Generate variables before querying the @combine's `query`.

    Arguments:
        obj: The object that contains the field that we are resolving,
          each key is a field name, e.g: {'team_id': 2510, 'team_name': 'Norwich City'}
        query_args: The query arguments of the field
        directive_args: The @combine's `argument` config

    Example:
      obj: {'team_id': 2510, 'team_name': 'Norwich City'}
      query_args: {apiKey: 'secret'}
      arguments: [
          {name: "team_id", field: "team_id"}
          {name: "apiKey", argument: "apiKey"}
      ]
    Returns: {'team_id': 2510, 'apiKey': 'secret'}
    """

    # With each dict in `directive_args`, use the "name" as the key,
    # If the dict has the "field", use data in `obj` as the value
    # Otherwise the dict should have the "argument" key, we will use data in `query_args` as the value
    return {
        arg['name']: obj[arg['field']]
        if 'field' in arg
        else query_args[arg['argument']]
        for arg in directive_args
    }


class CombineDirective(SchemaDirectiveVisitor):
    def visit_field_definition(
        self,
        field: GraphQLField,
        object_type: Union[GraphQLObjectType, GraphQLInterfaceType],
    ):
        config = CombineDirectiveInputSchema().load(self.args)

        def resolve_combine(current_object, info: GraphQLResolveInfo, **kwargs):
            """
            Arguments:
                current_object: The object that contains the field that we are resolving
                kwargs: The query variables
                info: Contains some helpful info:
                    - info.context: The context we passed in
                    - info.fields_nodes[0]: The field we are resolving
            """

            current_field: FieldNode = info.field_nodes[0]
            print('Name', current_field.name.value)

            query_variables = _generate_variables(
                current_object, query_args=kwargs, directive_args=config['arguments']
            )
            requested_query_data = _build_query(
                query_name=config['query'],
                variables=query_variables,
                requested_data=current_field.loc.source.body[
                    current_field.selection_set.loc.start : current_field.selection_set.loc.end
                ],
            )

            # Get current schema from the context we passed in
            schema = info.context['schema']

            success, result = graphql_sync(
                schema,
                requested_query_data,
                context_value=info.context,
                debug=app.debug,
            )

            if not success:
                logger.error(
                    message=f'Error when resolving @combine on field {info.field_name}',
                    data={'result': result},
                )
                return None

            # GraphQL result always returns {'data': {'queryName': requested_data} },
            # we only need the requested_data part
            return result['data'][config['query']]

        field.resolve = resolve_combine
        return field
