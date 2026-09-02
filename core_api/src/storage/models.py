from uuid import UUID
from enum import StrEnum
from sqlmodel import Field
from src.core.database import BaseModel


class FileStatusEnum(StrEnum):
    UPLOADING = "uploading_file"
    UPLOADED = "uploaded_file"
    FAILED = "failed_file"


class FileStatus(BaseModel, table=True):
    description: str = Field(nullable=False)


class File(BaseModel, table=True):
    filename: str = Field(nullable=False)
    size_bytes: int = Field(nullable=False, gt=0)
    storage_key: str = Field(nullable=False, unique=True)
    memoryspace_id: UUID = Field(
        index=True, nullable=False, foreign_key="memoryspace.id", ondelete="CASCADE"
    )
    status: UUID = Field(
        index=True, nullable=False, foreign_key="filestatus.id", ondelete="CASCADE"
    )
