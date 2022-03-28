from sqlalchemy import Index

from main import db
from main.models.base import TimestampMixin


class ProjectModel(db.Model, TimestampMixin):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    api_path = db.Column(db.String(64), unique=True)
    is_deployed = db.Column(db.Boolean, nullable=False, default=False)

    Index('idx_api_path', api_path)

    session = db.relationship('SessionModel', back_populates='project', uselist=False)

    def __init__(self, *args, **kwargs):
        super(ProjectModel, self).__init__(*args, **kwargs)
