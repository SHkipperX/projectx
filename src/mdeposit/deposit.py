from datetime import datetime, timedelta
from http.client import CREATED
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, status, HTTPException
from mdeposit.depschema import *
from setupdb.connectordb import get_session

router = APIRouter(prefix="/deposit")

async def __calcualtedeposit(depositschema: DepositSchemaCreate) -> dict[datetime: int]:
    """
    sP = P * i / 100 * T / K
    sP - итоговый расчёт
    P - изначальная сумма 
    i - годовая процентная ставка
    T - период в течении которого будут начислятся Р
    K - кол-во месяцев в году (12)
    """
    result = {}
    date = depositschema.date.date()
    P = depositschema.amount
    i = depositschema.rate / 100
    T = depositschema.periods
    K = 12
    for T in range(1, T + 1):
        futerdate = date + relativedelta(month=T)
        sP = P + (P * i * T / K)
        result[futerdate] = sP
    return result

@router.get("/get")
async def deposit_get(id: int = 1) -> dict:
    """
    Достаём из бд данные по `id` и прогоням через алгоритм Х
    Возвращаем набор `{datetime1: value1, datetime2: value2, ...}`
    """
    calc = __calcualtedeposit(...)
    return calc


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def deposit_create(deposit: DepositSchemaCreate, session=Depends(get_session)) -> dict:
    """
    Создание депозита
    """
    #depositDump = deposit.model_dump()
    """
    Добавляем объект в бд
    """
    calc = await __calcualtedeposit(deposit)

    return calc
    
@router.patch("/update", status_code=status.HTTP_201_CREATED)
async def deposit_update():
    ...