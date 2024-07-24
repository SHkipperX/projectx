from datetime import date
from pydantic import BaseModel, Field, field_validator

__all__ = [
    "DepositSchemaCreate",
]


class DepositSchema(BaseModel):
    deposit_date: str | date | None = Field(
        description="Дата заявки",
        examples=[
            "22.07.2077",
            "22.08.2077",
            "21.09.2077",
        ],
        alias="date",
    )

    @field_validator(
        "deposit_date",
    )
    @classmethod
    def format_date(cls, v: str) -> date:
        if isinstance(v, date):
            return v
        return date(*map(int, v.split(".")[::-1]))


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


class DepositResponse(DepositSchema):
    payment: int | None = Field(
        description="Выплата по вкладу",
        examples=[
            10008,
            10016,
            10025,
        ],
    )
