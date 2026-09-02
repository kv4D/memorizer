from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel
from pydantic import model_validator


# request schemas
class ChatCreateRequest(SQLModel):
    name: str
    memoryspace_id: UUID


class ChatEditRequest(SQLModel):
    name: str | None


class MessageCreateRequest(SQLModel):
    content: str
    chat_id: UUID


# response schemas
class ChatResponse(SQLModel):
    id: UUID
    name: str
    memoryspace_id: UUID
    created_at: datetime
    updated_at: datetime


class MessageResponse(SQLModel):
    id: UUID
    content: str
    chat_id: UUID
    created_at: datetime
    updated_at: datetime
