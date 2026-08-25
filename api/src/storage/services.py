from uuid import UUID
from datetime import date, datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import (
    get_password_hash,
    generate_access_token,
    generate_refresh_token,
    verify_password
)
from src.core.configs import api_settings


class StorageService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.refresh_token_repo = RefreshTokenRepository(session)
