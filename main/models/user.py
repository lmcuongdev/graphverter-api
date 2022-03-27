from sqlalchemy import Index

from main import db
from main.models.base import TimestampMixin


class UserModel(db.Model, TimestampMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)

    Index('idx_username', username)

    def __init__(self, *args, **kwargs):
        super(UserModel, self).__init__(*args, **kwargs)
