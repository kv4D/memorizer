from uuid import UUID
from datetime import date, datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import (
    get_password_hash,
    generate_access_token,
    generate_refresh_token,
    verify_password
)
from src.core.configs import api_settings
from .repositories import UserRepository, RefreshTokenRepository
from .models import User, RefreshToken


class UsersService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.refresh_token_repo = RefreshTokenRepository(session)

    async def get_user(self, user_id: UUID):
        user = await self.user_repo.get_by_id(user_id)

        if user is None:
            raise Exception("User not found")

        return user

    async def create_user(
        self,
        email: str,
        password: str,
        name: str,
        date_of_birth: date
    ):
        # hide password
        password_hashed = get_password_hash(password)

        user = User(
            email=email,
            date_of_birth=date_of_birth,
            password_hashed=password_hashed,
            name=name
        )
        user = await self.user_repo.add(user)

        return user

    async def create_tokens(self, user_id: UUID):
        access_token = generate_access_token(sub=user_id)
        refresh_token = generate_refresh_token(sub=user_id)

        # delete old refresh token
        old_token = await self.refresh_token_repo.get_by_user_id(user_id)
        if old_token:
            await self.refresh_token_repo.delete(old_token)
        
        # save new refresh token in the database    
        expire = datetime.now(timezone.utc) + timedelta(minutes=api_settings.API_ACCESS_TOKEN_EXPIRE_MINUTES)
        token = RefreshToken(
            user_id=user_id,
            expires_at=expire,
            token=refresh_token
            )
        await self.refresh_token_repo.add(token)

        return access_token, refresh_token

    async def register_user(
        self,
        email: str,
        password: str,
        name: str,
        date_of_birth: date
    ):
        user = await self.user_repo.get_by_email(email)

        if user:
            raise Exception("User with this email already exists")

        user = await self.create_user(email, password, name, date_of_birth)

        access_token, refresh_token = await self.create_tokens(user.id)

        return access_token, refresh_token

    async def login_user(
        self,
        email: str,
        password: str
    ):
        user = await self.user_repo.get_by_email(email)
        
        if user is None:
            raise Exception("Wrong email or password")
        
        verified = verify_password(password, user.password_hashed)
        
        if not verified:
            raise Exception("Wrong email or password")

        access_token, refresh_token = await self.create_tokens(user.id)

        return access_token, refresh_token
