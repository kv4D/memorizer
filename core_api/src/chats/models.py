from uuid import UUID
from sqlmodel import Field
from src.core.database import BaseModel


class Chat(BaseModel, table=True):
    name: str = Field(nullable=False, unique=True)
    memoryspace_id: UUID = Field(
        index=True, nullable=False, foreign_key="memoryspace.id", ondelete="CASCADE"
    )


class Message(BaseModel, table=True):
    content: str = Field(nullable=False)
    chat_id: UUID = Field(
        index=True, nullable=False, foreign_key="chat.id", ondelete="CASCADE"
    )
