from datetime import datetime
from sqlmodel import Field

from src.core.database import BaseModel


class User(BaseModel, table=True):
    email: str = Field(nullable=False, unique=True)
    password_hashed: str = Field(nullable=False)


class RefreshToken(BaseModel, table=True):
    token_hashed: str = Field(nullable=False)
    expires_at: datetime = Field(nullable=False)
