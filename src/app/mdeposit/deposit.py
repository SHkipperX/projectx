import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from src.app.mdeposit.depschema import DepositSchemaCreate
from src.app.mdeposit.depmodel import DepositModel
from src.app.setupdb.connectordb import get_session

deprouter = APIRouter(
    prefix="/deposit",
)


@deprouter.get(
    "/get",
    status_code=status.HTTP_200_OK,
)
async def deposit_get(
    id: int = 1,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Возвращает даты выплат депозита по уникальному `id` в виде `дата`: `сумма`
    """
    calc = {"2077-07-07": None}
    stmt = sql.select(DepositModel).where(DepositModel.deposit_id == id)
    async with session:
        result = await session.execute(stmt)
    result = result.scalar()
    if result:
        calc = await result.calculate()
    return calc


@deprouter.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
)
async def deposit_create(
    deposit: DepositSchemaCreate,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Создаёт депозит и возвращает ожидаемые выплаты в виде `дата`: `сумма`
    """
    deposit_dump = deposit.model_dump()
    stmt = sql.insert(DepositModel).values(deposit_dump)
    async with session:
        await session.execute(stmt)
        await session.commit()

    calc = await DepositModel(**deposit_dump).calculate()
    return calc
