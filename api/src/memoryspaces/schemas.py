from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel
from pydantic import model_validator


# request schemas
class MemoryspaceCreateRequest(SQLModel):
    name: str
    description: str = ""

    @model_validator(mode="after")
    def provide_description(self):
        self.description = f"{self.name}"
        return self


class MemoryspaceEditRequest(SQLModel):
    name: str | None = None
    description: str | None = None


# response schemas
class MemoryspaceResponse(SQLModel):
    id: UUID
    name: str
    description: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
