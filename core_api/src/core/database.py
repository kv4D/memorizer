from .configs import database_settings
from sqlmodel import SQLModel, Field, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import TIMESTAMP
from datetime import timezone, datetime
from typing import Type, TypeVar, Generic
from uuid import UUID, uuid4
from contextlib import asynccontextmanager


ENGINE = create_async_engine(database_settings.get_database_url())
SESSION_MAKER = async_sessionmaker(ENGINE, expire_on_commit=False)


class BaseModel(SQLModel, table=False):
    """
    Basic database model. 

    Must be used as a base for every single model.

    It doesn't create a table in the database, but works as a template for others.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=TIMESTAMP(timezone=True)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
        sa_type=TIMESTAMP(timezone=True)
    )


ModelT = TypeVar('ModelT', bound=BaseModel)


class BaseRepository(Generic[ModelT]):
    """Base repository that is being used throughout all repositories."""

    def __init__(self, session: AsyncSession, model_type: Type[ModelT]):
        self.session = session
        self.model_type = model_type

    async def add(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def get_by_id(self, entity_id: UUID) -> ModelT | None:
        entity = await self.session.get(self.model_type, entity_id)
        return entity

    async def get_all(self) -> list[ModelT] | None:
        statement = select(self.model_type)
        result = await self.session.execute(statement)
        entities = result.scalars().all()
        return list(entities)

    async def update(self, entity: ModelT, new_data: dict) -> ModelT:
        for key, value in new_data.items():
            setattr(entity, key, value)

        self.session.add(entity)
        return entity

    async def delete(self, entity: ModelT) -> ModelT:
        await self.session.delete(entity)
        return entity


@asynccontextmanager
async def unit_of_work():
    """
    Centralized method of controlling database transactions.

    Use when you have to work with database.

    Yields a database session for your purposes, closes session on exit.

    If there was an exception - rollbacks the changes you've made, 
    otherwise - makes a commit.
    """
    session: AsyncSession = SESSION_MAKER()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
