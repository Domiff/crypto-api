from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings.config import settings

fast_api_engine = create_async_engine(settings.database.db_url)
async_session = async_sessionmaker(fast_api_engine, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def create_celery_sessionmaker():
    celery_engine = create_async_engine(
        settings.database.db_url,
        pool_pre_ping=True,
    )
    return async_sessionmaker(celery_engine, expire_on_commit=False)
