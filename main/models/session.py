from sqlalchemy import Index

from main import db
from main.models.base import MetaDataMixin, TimestampMixin


class Session(db.Model, TimestampMixin, MetaDataMixin):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    project = db.relationship('ProjectModel', foreign_keys=[project_id])
