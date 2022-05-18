from flask import jsonify

import main.engines.project as project_engine
from main import app, db
from main.common.decorators import user_authenticated, validate_input, validate_project
from main.common.exceptions import BadRequest
from main.schemas.base import PaginationSchema
from main.schemas.project import (
    CreateProjectSchema,
    ProjectDetailSchema,
    ProjectsSchema,
    UpdateProjectSchema,
)


@app.route('/projects', methods=['POST'])
@user_authenticated
@validate_input(CreateProjectSchema())
def create_project(args, user, **__):
    if project_engine.get_project(api_path=args['api_path']):
        raise BadRequest(error_message='API path is already taken.')

    project = project_engine.create_project(
        user_id=user.id, name=args['name'], api_path=args['api_path']
    )
    db.session.commit()
    project_engine.init_project(project.id)

    return jsonify({'id': project.id})


@app.route('/projects', methods=['GET'])
@user_authenticated
@validate_input(PaginationSchema())
def get_projects(args, user, **__):
    """Get a project list with filters"""
    extra_filters = {'user_ids': [user.id]}
    projects = project_engine.get_projects({**args, **extra_filters})
    return ProjectsSchema().jsonify(projects)


@app.route('/projects/<int:project_id>', methods=['GET'])
@user_authenticated
@validate_project
def get_project(project, **__):
    return ProjectDetailSchema().jsonify(project)


@app.route('/projects/<int:project_id>', methods=['PUT'])
@user_authenticated
@validate_project
@validate_input(UpdateProjectSchema())
def update_project(args, project, **__):
    if 'api_path' in args and project_engine.get_project(api_path=args['api_path']):
        raise BadRequest(error_message='API path is already taken.')
    project = project_engine.update_project(project, **args)
    return ProjectDetailSchema().jsonify(project)
