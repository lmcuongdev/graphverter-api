from datetime import datetime, timedelta
from typing import Optional

import jwt
from flask import request
from flask_bcrypt import check_password_hash
from jwt import PyJWTError

from main import config
from main.common.exceptions import (
    BadRequest,
    InvalidAccessToken,
    InvalidAuthorizationHeader,
    InvalidCredentials,
)
from main.libs.log import ServiceLogger
from main.models.user import UserModel

logger = ServiceLogger(__name__)


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


def parse_access_token() -> str:
    # Parse authorization header and get access token from the format: Bearer <access_token>
    authorization = None

    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']

    if not authorization:
        raise InvalidAuthorizationHeader()

    if not authorization.startswith('Bearer '):
        raise InvalidAccessToken()
    # Parse access token from the authorization header
    return authorization[len('Bearer ') :].lstrip()


def get_user(access_token: str) -> Optional[UserModel]:
    try:
        payload = jwt.decode(access_token, config.JWT_SECRET, algorithms='HS256')
        user_id = payload['iss']
    except PyJWTError as e:
        logger.info(message=str(e))
        raise InvalidAccessToken()

    user = UserModel.query.get(user_id)
    if not user:
        raise InvalidAccessToken()

    return user
