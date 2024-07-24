import pytest
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import Client, Response
from src.app.mdeposit.depmodel import DepositModel


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date,amount,periods,rate",
    [
        ("01.01.2021", 10_000, 1, 1),
        ("31.03.2021", 3_000_000, 60, 8),
        ("31.12.1000", 228_123, 13, 3.333),
    ],
)
async def test_on_create(
    client: Client,
    session: AsyncSession,
    date,
    amount,
    periods,
    rate,
):
    response: Response = await client.post(
        "/deposit/create",
        json={
            "date": date,
            "amount": amount,
            "periods": periods,
            "rate": rate,
        },
    )
    stmt = sql.select(DepositModel)
    async with session() as session:
        result = await session.execute(stmt)
    result = result.scalar()
    calc = await result.calculate()
    assert response.json() == calc


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date,amount,periods,rate",
    [
        ("Pepe", 10_000, 1, 1),
        ("31.03.2021", 30_000_000, 60, 8),
        ("31.12.1000", 1, 13, 3.333),
        ("12.03.2031", 10_000, 0.5, 1),
        ("12.03.2031", 10_000, 1, 0.5),
        ("12.03.2031", 10_000, 60.5, 1),
        ("12.03.2031", 10_000, 1, 8.5),
    ],
)
async def test_on_uncreate(
    client: Client,
    session: AsyncSession,
    date,
    amount,
    periods,
    rate,
):
    response: Response = await client.post(
        "/deposit/create",
        json={
            "date": date,
            "amount": amount,
            "periods": periods,
            "rate": rate,
        },
    )
    stmt = sql.select(DepositModel)
    async with session() as session:
        result = await session.execute(stmt)
    result = result.scalar()
    assert result is None
    assert response.json() == {"error": "описание ошибки"}
