from uuid import UUID
from fastapi import APIRouter, Depends

from src.core.database import unit_of_work
from src.core.dependencies import get_current_user_from_access_token

from .services import MemoryspacesService
from .schemas import (
    MemoryspaceCreateRequest,
    MemoryspaceResponse,
    MemoryspaceEditRequest,
)

memoryspaces_router = APIRouter(prefix="/memoryspaces", tags=["memoryspaces"])


@memoryspaces_router.post("", response_model=MemoryspaceResponse)
async def create_new_memoryspace(
    memoryspace_data: MemoryspaceCreateRequest,
    user_id: UUID = Depends(get_current_user_from_access_token),
):
    async with unit_of_work() as session:
        service = MemoryspacesService(session)
        name = memoryspace_data.name
        description = memoryspace_data.description
        memoryspace = await service.create_memoryspace(user_id, name, description)
    return memoryspace


@memoryspaces_router.get("", response_model=list[MemoryspaceResponse])
async def get_user_memoryspaces(
    user_id: UUID = Depends(get_current_user_from_access_token),
):
    async with unit_of_work() as session:
        service = MemoryspacesService(session)
        memoryspace = await service.get_user_memoryspaces(user_id)
    return memoryspace


@memoryspaces_router.get("/{memoryspace_id}", response_model=MemoryspaceResponse)
async def get_memoryspace(memoryspace_id: UUID):
    async with unit_of_work() as session:
        service = MemoryspacesService(session)
        memoryspace = service.get_memoryspace(memoryspace_id)
    return memoryspace


@memoryspaces_router.get("/{memoryspace_id}/chats")
async def get_memoryspace_chats(memoryspace_id: UUID):
    async with unit_of_work() as session:
        service = MemoryspacesService(session)
    pass


@memoryspaces_router.patch("/{memoryspace_id}")
async def edit_memoryspace(
    memoryspace_id: UUID, new_memoryspace_data: MemoryspaceEditRequest
):
    async with unit_of_work() as session:
        service = MemoryspacesService(session)
        memoryspace = await service.edit_memoryspace(
            memoryspace_id, new_memoryspace_data.model_dump()
        )
    return memoryspace


@memoryspaces_router.delete("/{memoryspace_id}", response_model=MemoryspaceResponse)
async def delete_memoryspace(memoryspace_id: UUID):
    async with unit_of_work() as session:
        service = MemoryspacesService(session)
        memoryspace = service.delete_memoryspace(memoryspace_id)
    return memoryspace
