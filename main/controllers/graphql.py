from ariadne import gql, graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import jsonify, request

from main import app
from main.directives.anonymize import AnonymizeDirective
from main.directives.rest import RestDirective
from main.engines.project import get_project
from main.engines.version import get_latest_version
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

    # TODO: Load from cache, api_path->schema_text
    project = get_project(api_path=api_path)
    # if not project or not project.is_deployed:
    #     raise NotFound(error_message='No published project for this path found.')
    version = get_latest_version(project_id=project.id)

    type_defs = gql(version.schema_text)
    schema = make_executable_schema(
        type_defs,
        directives={'anonymize': AnonymizeDirective, 'rest': RestDirective},
    )

    success, result = graphql_sync(
        schema, request_query, context_value=request, debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
