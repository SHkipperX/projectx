import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine

from src.app.app import app
from src.app.mdeposit.depmodel import DepositModel
from src.app.conf import DBconfinit
from src.app.setupdb.connectordb import async_session_maker


async def async_engine():
    return create_async_engine(
        url=DBconfinit.get_db_url_test,
    )


async def setup(engine):
    async with engine.begin() as conn:
        await conn.run_sync(DepositModel.metadata.create_all)


async def teardown(engine):
    async with engine.begin() as conn:
        await conn.run_sync(DepositModel.metadata.drop_all)


@pytest_asyncio.fixture
async def session():
    engine = await async_engine()
    await setup(engine)
    yield async_session_maker
    await teardown(engine)


@pytest_asyncio.fixture(
    scope="function",
    autouse=False,
)
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
