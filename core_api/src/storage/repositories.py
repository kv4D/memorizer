from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import BaseRepository
from .models import File


class FileRepository(BaseRepository[File]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_type=File)
