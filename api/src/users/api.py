from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.database import unit_of_work
from src.core.dependencies import get_current_user_from_access_token
from .services import UsersService
from .schemas import RegistrationRequest, TokenResponse, UserResponse

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    user_id: UUID = Depends(get_current_user_from_access_token),
):
    async with unit_of_work() as session:
        service = UsersService(session)
        user = await service.get_user(user_id)
    return user


@users_router.post("/login", response_model=TokenResponse)
async def login(user_data: OAuth2PasswordRequestForm = Depends()):
    async with unit_of_work() as session:
        service = UsersService(session)
        email = user_data.username
        password = user_data.password
        access_token, refresh_token = await service.login_user(email, password)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@users_router.post("/register", response_model=TokenResponse)
async def register(user_data: RegistrationRequest):
    async with unit_of_work() as session:
        service = UsersService(session)
        access_token, refresh_token = await service.register_user(
            **user_data.model_dump(exclude_unset=True)
        )
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@users_router.post("/refresh", response_model=TokenResponse)
async def refresh_access(user_id: UUID = Depends(get_current_user_from_access_token)):
    async with unit_of_work() as session:
        service = UsersService(session)
        access_token, refresh_token = await service.create_tokens(user_id)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
