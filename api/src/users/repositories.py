from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.core.database import BaseRepository
from .models import User, RefreshToken


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_type=User)
    
    async def get_by_email(self, email: str):
        statement = select(self.model_type).where(self.model_type.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_type=RefreshToken)

    async def get_by_user_id(self, user_id: UUID) -> RefreshToken | None:
        statement = select(self.model_type).where(self.model_type.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()