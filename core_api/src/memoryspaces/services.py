from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .repositories import MemoryspaceRepository
from .models import Memoryspace


class MemoryspacesService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.memoryspace_repo = MemoryspaceRepository(session)

    async def create_memoryspace(self, user_id: UUID, name: str, description: str):
        memoryspace = Memoryspace(name=name, description=description, owner_id=user_id)

        memoryspace = await self.memoryspace_repo.add(memoryspace)

        return memoryspace

    async def get_user_memoryspaces(self, user_id: UUID):
        return await self.memoryspace_repo.get_memoryspace_by_user_id(user_id)

    async def get_memoryspace(self, memoryspace_id: UUID):
        memoryspace = await self.memoryspace_repo.get_by_id(memoryspace_id)

        if memoryspace is None:
            raise Exception("Memoryspace is not found")

        return memoryspace

    async def edit_memoryspace(self, memoryspace_id: UUID, new_data: dict):
        memoryspace = await self.get_memoryspace(memoryspace_id)

        memoryspace = await self.memoryspace_repo.update(memoryspace, new_data)

        return memoryspace

    async def delete_memoryspace(self, memoryspace_id: UUID):
        memoryspace = await self.get_memoryspace(memoryspace_id)

        await self.memoryspace_repo.delete(memoryspace)

        return memoryspace
