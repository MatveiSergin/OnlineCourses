from typing import AsyncGenerator
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import engine, ModelORM, db_session
from database.models import UsersORM


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(ModelORM.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_session() as session:
        yield session


async def get_user_db():
    async with db_session() as session:
        yield SQLAlchemyUserDatabase(session, UsersORM)
