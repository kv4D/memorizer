from .models import Chat, Message
from src.core.database import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    def __init__(self, session):
        super().__init__(session, model_type=Chat)


class MessageRepository(BaseRepository[Message]):
    def __init__(self, session):
        super().__init__(session, model_type=Message)
