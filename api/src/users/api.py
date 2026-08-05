from fastapi import APIRouter, Depends


users_router = APIRouter(prefix="/users", tags=["users"])
