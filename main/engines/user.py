from werkzeug.security import generate_password_hash

from main import db
from main.models.user import UserModel


def create_user(username: str, password: str, **kwargs) -> UserModel:
    hash_password = generate_password_hash(password)
    user = UserModel(username=username, password=hash_password, **kwargs)

    db.session.add(user)
    return user
