from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Chat
from .repositories import ChatRepository, MessageRepository


class ChatsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.chat_repo = ChatRepository(session)
        self.message_repo = MessageRepository(session)

    async def get_chat(self, chat_id: UUID):
        chat = await self.chat_repo.get_by_id(chat_id)

        if chat is None:
            raise Exception("Chat was not found")

        return chat

    async def delete_chat(self, chat_id: UUID):
        chat = await self.get_chat(chat_id)

        await self.chat_repo.delete(chat)

        return chat

    async def create_chat(self, name: str, memoryspace_id: UUID):
        chat = Chat(name=name, memoryspace_id=memoryspace_id)

        chat = await self.chat_repo.add(chat)

        return chat

    async def get_chat_messages(self, chat_id: UUID):
        await self.get_chat(chat_id)

        messages = await self.message_repo.get_messages_by_chat_id(chat_id)

        return messages
