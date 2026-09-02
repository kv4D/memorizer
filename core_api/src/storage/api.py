from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.database import unit_of_work
from src.core.dependencies import get_current_user_from_access_token
from .services import StorageService


storage_router = APIRouter(prefix="/storage", tags=["storage"])
