"""Security related tools."""
from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from pwdlib import PasswordHash

from .configs import api_settings


def _generate_jwt_token(data: dict) -> str:
    """
    Base for jwt token generation. Only for internal purposes.

    Args:
        data (dict): _description_

    Returns:
        str: the token
    """
    # TODO: maybe add data checks
    token = jwt.encode(
        data,
        key=api_settings.API_SECRET_KEY,
        algorithm=api_settings.API_ALGORITHM
    )
    return token


def generate_access_token(sub: Any, data: dict | None = None) -> str:
    """
    Generate an access token.

    Args:
        sub (Any): your unique identifier, ID
        data (dict): extra piece of information

    Returns:
        str: the token
    """
    data_to_encode = data.copy() if data else {}
    expire = datetime.now(
        timezone.utc) + timedelta(minutes=api_settings.API_ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update(
        {
            "exp": expire,
            "sub": str(sub),
            "type": "access"
        }
    )
    access_token = _generate_jwt_token(data_to_encode)
    return access_token


def generate_refresh_token(sub: Any, data: dict | None = None) -> str:
    """
    Generate a refresh token.

    Args:
        sub (Any): your unique identifier, ID
        data (dict): extra piece of information

    Returns:
        str: the token
    """
    data_to_encode = data.copy() if data else {}
    expire = datetime.now(
        timezone.utc) + timedelta(minutes=api_settings.API_REFRESH_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update(
        {
            "exp": expire,
            "sub": str(sub),
            "type": "access"
        }
    )
    refresh_token = _generate_jwt_token(data_to_encode)
    return refresh_token


def decode_token(token: str) -> dict:
    """Decodes a token.

    Args:
        token (str): the token you have (access or refresh)

    Returns:
        dict: payload, data that was extracted from a decoded token
    """
    payload = jwt.decode(token,
                         api_settings.API_SECRET_KEY,
                         algorithms=[api_settings.API_ALGORITHM])
    return payload


PASSWORDS_HASH = PasswordHash.recommended()


def get_password_hash(unhashed_password: str) -> str:
    password_hash = PASSWORDS_HASH.hash(unhashed_password)
    return password_hash


def verify_password(unhashed_password: str, password_hash: str) -> bool:
    """
    Checks if a provided password matches the hashed password. 

    Returns:
        bool: true if hashes match (it means password is correct)
    """
    is_verified = PASSWORDS_HASH.verify(unhashed_password, password_hash)
    return is_verified
