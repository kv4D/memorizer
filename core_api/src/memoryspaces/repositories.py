from uuid import UUID
from sqlmodel import select

from .models import Memoryspace
from src.core.database import BaseRepository


class MemoryspaceRepository(BaseRepository[Memoryspace]):
    def __init__(self, session):
        super().__init__(session, model_type=Memoryspace)

    async def get_memoryspace_by_user_id(self, user_id: UUID) -> list[Memoryspace]:
        statement = select(self.model_type).where(self.model_type.owner_id == user_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())
