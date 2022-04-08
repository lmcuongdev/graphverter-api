from typing import Optional

from main import config, db
from main.engines.session import create_session
from main.engines.version import (
    create_version,
    get_latest_version,
    update_latest_version,
)
from main.enums import VersionStatus
from main.libs.log import ServiceLogger
from main.models.project import ProjectModel
from main.models.version import VersionModel

logger = ServiceLogger(__name__)


def get_project(
    project_id: Optional[int] = None, api_path: Optional[str] = None
) -> Optional[ProjectModel]:
    if project_id is None and api_path is None:
        return None
    if project_id:
        return ProjectModel.query.get(project_id)
    # TODO: Cache with project_id and api_path
    return ProjectModel.query.filter(ProjectModel.api_path == api_path).first()


def create_project(user_id: int, name: str, api_path: str, **__) -> ProjectModel:
    project = ProjectModel(user_id=user_id, name=name, api_path=api_path, **__)
    db.session.add(project)

    return project


def init_project(project_id: int):
    create_session(project_id, meta_data={})
    db.session.commit()


def get_projects(filters: dict) -> dict:
    """
    Get a list of channels that satisfies criteria
    """
    items_per_page = filters.get('items_per_page', config.DEFAULT_ITEMS_PER_PAGE)
    page = filters.get('page', 1)
    query = ProjectModel.query

    query_filters = []

    # Filter by user ids if it's set
    user_ids = filters.get('user_ids')
    if user_ids:
        query_filters.append(ProjectModel.user_id.in_(user_ids))

    # Build pagination
    query = query.filter(*query_filters)
    total_projects = query.count()
    projects = query.paginate(page, items_per_page, False).items

    return {
        'page': page,
        'total_items': total_projects,
        'items_per_page': items_per_page,
        'items': projects,
    }


def deploy_project(project_id: int) -> VersionModel:
    """Deploy the project and return newly created version"""
    logger.info(message='Start deploying project', data={'project_id': project_id})

    project = get_project(project_id)
    session = project.session
    # TODO: Validate schema text

    current_version = get_latest_version(project_id=project_id)
    if current_version and not current_version.is_dirty:
        logger.info(
            message='Deployed successfully',
            data={'project_id': project_id, 'version_id': current_version.id},
        )
        return current_version
    # Deactivate current version before creating new active version
    update_latest_version(
        project_id=project_id,
        status=VersionStatus.INACTIVE,
    )

    version = create_version(
        project_id=project_id,
        status=VersionStatus.ACTIVE,
        is_dirty=False,
        version_data={
            'schema_text': session.meta_data['schema_text'],
            'api_path': project.api_path,
        },
    )
    db.session.commit()
    logger.info(
        message='Deployed successfully',
        data={'project_id': project_id, 'version_id': version.id},
    )

    return version
