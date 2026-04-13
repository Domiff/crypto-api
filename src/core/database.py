from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings

fast_api_engine = create_async_engine(settings.DB_URL)
async_session = async_sessionmaker(fast_api_engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def create_celery_sessionmaker() -> async_sessionmaker[AsyncSession]:
    celery_engine = create_async_engine(settings.DB_URL, pool_pre_ping=True)
    return async_sessionmaker(celery_engine, expire_on_commit=False)


async def ping_database() -> bool:
    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
