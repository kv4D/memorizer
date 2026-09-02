from uuid import UUID
from fastapi import APIRouter, Depends

from src.core.database import unit_of_work
from src.core.dependencies import get_current_user_from_access_token
from .services import ChatsService
from .schemas import ChatResponse, ChatEditRequest, ChatCreateRequest

chats_router = APIRouter(prefix="/chats", tags=["chats"])


@chats_router.post("", dependencies=[Depends(get_current_user_from_access_token)])
async def create_new_chat(chat_data: ChatCreateRequest):
    async with unit_of_work() as session:
        service = ChatsService(session)
        name = chat_data.name
        memoryspace_id = chat_data.memoryspace_id
        chat = await service.create_chat(name, memoryspace_id)
    return chat


@chats_router.get("/{chat_id}")
async def get_chat(chat_id: UUID):
    async with unit_of_work() as session:
        service = ChatsService(session)
        chat = await service.get_chat(chat_id)
    return chat


@chats_router.delete("/{chat_id}", response_model=ChatResponse)
async def delete_chat(chat_id: UUID):
    async with unit_of_work() as session:
        service = ChatsService(session)
        chat = await service.delete_chat(chat_id)
    return chat


@chats_router.post("/{chat_id}/messages")
async def send_message(chat_id: UUID):
    async with unit_of_work() as session:
        service = ChatsService(session)
    pass


@chats_router.get("/{chat_id}/messages", response_model=list[ChatResponse])
async def get_chat_messages(chat_id: UUID):
    async with unit_of_work() as session:
        service = ChatsService(session)
        messages = await service.get_chat_messages(chat_id)
    return messages
