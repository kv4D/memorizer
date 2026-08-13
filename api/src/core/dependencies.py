from uuid import UUID
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from .security import decode_token

# --------- web level dependencies ---------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


async def _get_user_id_from_token(token: str):
    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise ValueError("Invalid token type")

        user_id = payload.get("sub")
        if user_id is None:
            raise jwt.InvalidTokenError
        return UUID(user_id)
    except Exception as exc:
        credentials_exception = ValueError(
            "Could not validate credentials ({exc})",
        )
        raise credentials_exception from exc


async def get_current_user_from_access_token(
    access_token: str = Depends(oauth2_scheme)
) -> UUID:
    return await _get_user_id_from_token(access_token)


async def get_current_user_from_refresh_token(
    refresh_token: str
) -> UUID:
    return await _get_user_id_from_token(refresh_token)
