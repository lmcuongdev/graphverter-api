from sqlalchemy import Index
from sqlalchemy.dialects import mysql

from main import db
from main.libs.log import ServiceLogger

from .base import MetaDataMixin, TimestampMixin

logger = ServiceLogger(__name__)


class VersionModel(db.Model, TimestampMixin, MetaDataMixin):
    __tablename__ = 'version'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer,
        db.ForeignKey('project.id'),
        nullable=False,
    )
    status = db.Column(db.String(32), nullable=False)
    is_dirty = db.Column(db.Boolean, default=False)
    _meta_data = db.Column('meta_data', mysql.MEDIUMTEXT, nullable=True)

    project = db.relationship('ProjectModel', foreign_keys=[project_id])

    Index('idx_version_project', project_id)

    def __init__(self, *args, **kwargs):
        super(VersionModel, self).__init__(*args, **kwargs)

    @property
    def schema_text(self, *_, **__) -> str:
        return self.meta_data['schema_text']
