from uuid import UUID
from sqlmodel import select

from .models import Chat, Message
from src.core.database import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    def __init__(self, session):
        super().__init__(session, model_type=Chat)


class MessageRepository(BaseRepository[Message]):
    def __init__(self, session):
        super().__init__(session, model_type=Message)

    async def get_messages_by_chat_id(self, chat_id: UUID):
        statement = select(self.model_type).where(self.model_type.chat_id == chat_id)

        result = await self.session.execute(statement)

        return list(result.scalars().all())
