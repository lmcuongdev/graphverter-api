from datetime import datetime, timedelta

import jwt
from werkzeug.security import check_password_hash

from main import config
from main.common.exceptions import BadRequest, InvalidCredentials
from main.models.user import UserModel


def validate_username(username: str):
    # Check if username existed
    user = UserModel.query.filter(UserModel.username == username).first()
    if user:
        raise BadRequest(error_message='Username already existed.')


def create_access_token(
    user: UserModel, lifetime: int = config.ACCESS_TOKEN_LIFETIME
) -> str:
    iat = datetime.utcnow()

    return jwt.encode(
        {
            'iss': user.id,
            'iat': iat,
            'exp': iat + timedelta(seconds=lifetime),
        },
        config.JWT_SECRET,
    )


def get_login_user(username: str, password: str) -> UserModel:
    user = UserModel.query.filter(UserModel.username == username).first()

    if not user:
        raise InvalidCredentials(error_message='Username not found.')

    if not check_password_hash(user.password, password):
        raise InvalidCredentials()

    return user
