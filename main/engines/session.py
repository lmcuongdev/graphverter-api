from typing import List

from main import db
from main.engines.version import update_latest_version
from main.models.session import SessionModel


def create_session(project_id: int, **kwargs) -> SessionModel:
    session = SessionModel(project_id=project_id, **kwargs)
    db.session.add(session)
    return session


def get_session(session_id: int) -> SessionModel:
    return SessionModel.query.get(session_id)


def update_session(
    session: SessionModel, schema_text: str = None, endpoints: List[dict] = None
):
    meta_data = session.meta_data
    if schema_text:
        meta_data['schema_text'] = schema_text
    if endpoints:
        meta_data['endpoints'] = endpoints
    session.meta_data = meta_data

    update_latest_version(session.project_id, is_dirty=True)

    db.session.commit()
