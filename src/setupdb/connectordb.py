from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine,  AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from conf import DBconfinit

engine = create_async_engine(
    url=DBconfinit.get_db_url,
    poolclass=NullPool,
)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
