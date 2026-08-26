from datetime import date, datetime
from sqlmodel import SQLModel, Field
from pydantic import EmailStr


# request schemas
class RegistrationRequest(SQLModel):
    email: EmailStr
    password: str
    name: str
    date_of_birth: date


# response schemas
class TokenResponse(SQLModel):
    refresh_token: str
    access_token: str
    token_type: str = "bearer"


class UserResponse(SQLModel):
    email: str
    name: str
    date_of_birth: date
    created_at: datetime
    updated_at: datetime
