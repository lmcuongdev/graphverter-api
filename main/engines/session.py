from sqlalchemy import desc

from main import db
from main.models.session import SessionModel


def create_session(project_id: int, **kwargs) -> SessionModel:
    session = SessionModel(project_id=project_id, **kwargs)
    db.session.add(session)
    return session


def get_session(project_id: int) -> SessionModel:
    return (
        SessionModel.query.filter(SessionModel.project_id == project_id)
        .order_by(desc(SessionModel.id))
        .first()
    )
