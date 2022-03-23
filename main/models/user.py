from sqlalchemy import Index

from main import db
from main.models.base import TimestampMixin


class User(db.Model, TimestampMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)

    Index('idx_email', email)
    Index('idx_username', username)
