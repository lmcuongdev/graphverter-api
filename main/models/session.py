from main import db
from main.models.base import MetaDataMixin, TimestampMixin


class SessionModel(db.Model, TimestampMixin, MetaDataMixin):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer,
        db.ForeignKey('project.id'),
        nullable=False,
    )

    project = db.relationship(
        'ProjectModel', foreign_keys=[project_id], back_populates='session'
    )

    def __init__(self, *args, **kwargs):
        super(SessionModel, self).__init__(*args, **kwargs)
