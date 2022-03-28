from typing import Optional

from main import config, db
from main.engines.session import create_session
from main.models.project import ProjectModel


def get_project(
    project_id: Optional[str] = None, api_path: Optional[str] = None
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
    user_ids = filters.get('organization_ids')
    if user_ids:
        query_filters.append(ProjectModel.organization_id.in_(user_ids))

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
