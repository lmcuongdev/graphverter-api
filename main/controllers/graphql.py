from ariadne import graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import jsonify, request

from main import app
from main.directives.anonymize import AnonymizeDirective
from main.directives.rest import RestDirective
from main.engines.project import get_schema_text
from main.libs.log import ServiceLogger

logger = ServiceLogger(__name__)


@app.route('/graphql', methods=['GET'])
def get_graphql_playground(*_, **__):
    return PLAYGROUND_HTML


@app.route('/<api_path>/graphql', methods=['POST'])
def execute_graphql(api_path: str, **__):
    request_query = request.get_json()
    if request_query.get('operationName') != 'IntrospectionQuery':
        # If this is not an introspection query,
        # TODO: send event or do some analytics work here
        logger.info(message='Got query', data=request_query)

    # Assume the schema_text is valid because validation on this should be done in config time, not runtime
    schema_text = get_schema_text(api_path)
    schema = make_executable_schema(
        type_defs=schema_text,
        directives={'anonymize': AnonymizeDirective, 'rest': RestDirective},
    )

    success, result = graphql_sync(
        schema, request_query, context_value=request, debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
