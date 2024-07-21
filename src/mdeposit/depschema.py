from datetime import datetime
from pydantic import BaseModel, Field


__all__ = [
    "DepositSchemaCreate",
    "DepositSchemaExample",
]


class DepositSchema(BaseModel):
    date: datetime = Field(
        description="Дата заявки",
    )


class DepositSchemaCreate(DepositSchema):
    periods: int = Field(
        description="Количество месяцев по вкладу",
        le=60,
        ge=1,
    )
    amount: int = Field(
        description="Сумма вклада",
        le=3_000_000,
        ge=10_000,
    )
    rate: float = Field(
        description="Процент по вкладу",
        le=8,
        ge=1,
    )


class DepositSchemaExample(DepositSchema): ...
