from main import app
from main.common.decorators import (
    user_authenticated,
    validate_input,
    validate_project,
    validate_session,
)
from main.engines.session import update_session
from main.schemas.session import SessionSchema, UpdateSessionSchema


@app.route('/projects/<int:project_id>/sessions/<int:session_id>', methods=['PUT'])
@user_authenticated
@validate_project
@validate_session
@validate_input(UpdateSessionSchema())
def update_schema_text(args, session, *_, **__):
    update_session(session, schema_text=args['schema_text'])
    return SessionSchema().jsonify(session)


@app.route('/projects/<int:project_id>/sessions/<int:session_id>', methods=['GET'])
@user_authenticated
@validate_project
@validate_session
def get_session(session, *_, **__):
    return SessionSchema().jsonify(session)
