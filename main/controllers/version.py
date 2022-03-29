from flask import jsonify

from main import app
from main.common.decorators import user_authenticated, validate_project
from main.common.exceptions import BadRequest
from main.engines.project import deploy_project
from main.engines.version import get_latest_version as get_latest_version_
from main.schemas.version import VersionSchema


@app.route('/projects/<int:project_id>/versions', methods=['POST'])
@user_authenticated
@validate_project
def deploy(project_id, *_, **__):
    version = deploy_project(project_id)
    return jsonify({'id': version.id})


@app.route('/projects/<int:project_id>/versions/latest', methods=['GET'])
@user_authenticated
@validate_project
def get_latest_version(project_id, *_, **__):
    # Get latest version and check whether it's dirty or not
    version = get_latest_version_(project_id)
    if not version:
        raise BadRequest(error_message='Latest version is not found.')

    return VersionSchema().jsonify(version)
