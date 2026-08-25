from uuid import UUID
from fastapi import APIRouter, Depends

from src.core.database import unit_of_work
from src.core.dependencies import get_current_user_from_access_token


memoryspaces_router = APIRouter(prefix="/memoryspaces", tags=["memoryspaces"])