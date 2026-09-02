from uuid import UUID
from datetime import datetime, date
from sqlmodel import Field
from sqlalchemy import TIMESTAMP

from src.core.database import BaseModel



class User(BaseModel, table=True):
    email: str = Field(nullable=False, unique=True)
    password_hashed: str = Field(nullable=False)
    name: str = Field(nullable=False)
    date_of_birth: date


class RefreshToken(BaseModel, table=True):
    user_id: UUID = Field(
        index=True, 
        nullable=False, 
        foreign_key="user.id",
        ondelete="CASCADE"
        )
    token: str = Field(nullable=False)
    expires_at: datetime = Field(nullable=False, sa_type=TIMESTAMP(timezone=True))
