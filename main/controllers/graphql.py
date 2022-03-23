from ariadne import QueryType, gql, graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import jsonify, request

from main import app
from main.directives.anonymize import AnonymizeDirective
from main.directives.rest import RestDirective


@app.route('/new', methods=['GET'])
def ping(*_, **__):
    # res = request.get_json(silent=True)
    print(request.args)
    return jsonify([{'name': 'email', 'value': 'ryan@mail.com'}])


@app.route('/data', methods=['POST'])
def data(*_, **__):
    res = request.get_json(silent=True)
    print(res['data'])
    return jsonify(res['data'])


@app.route('/graphql', methods=['GET'])
def get_graphql_playground(*_, **__):
    return PLAYGROUND_HTML


@app.route('/graphql', methods=['POST'])
def graphql_server(*_, **__):
    request_query = request.get_json()
    with open('rest.graphql', 'r') as f:
        type_defs = gql(f.read())

    query = QueryType()

    schema = make_executable_schema(
        type_defs,
        query,
        directives={'anonymize': AnonymizeDirective, 'rest': RestDirective},
    )

    # q = '{query: me{id, full_name}}'
    # request_query = {
    #     'query': '{me(authToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjU0LCJhdWQiOiJtZW1iZXIiLCJpYXQiOjE2NDY2NzM1ODcsImV4cCI6MTY0NjY3NTM4NywiZnJlc2giOnRydWV9.PL0JoIvKnuQj2MrMz9OqgjVDzh29-nSX_gOPX34IgqU"){id, full_name, email, onboarding{flow}, organization{name, subdomain}}}'}
    success, result = graphql_sync(
        schema, request_query, context_value=request, debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
