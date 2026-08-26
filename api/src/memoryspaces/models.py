from uuid import UUID
from sqlmodel import Field
from src.core.database import BaseModel


class Memoryspace(BaseModel, table=True):
    name: str = Field(nullable=False)
    description: str
    owner_id: UUID = Field(
        index=True, nullable=False, foreign_key="user.id", ondelete="CASCADE"
    )
