from datetime import date, timedelta
from sqlalchemy import Integer, Date, Float
from sqlalchemy.orm import mapped_column, Mapped

from src.app.setupdb.metadb import BASE

__all__ = []


class DepositModel(BASE):
    __tablename__ = "deposit"

    deposit_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    deposit_date: Mapped[date] = mapped_column(
        Date(),
    )

    periods: Mapped[int] = mapped_column(
        Integer(),
    )

    amount: Mapped[int] = mapped_column(
        Integer(),
    )

    rate: Mapped[float] = mapped_column(
        Float(),
    )

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>(id={self.deposit_id})"

    async def calculate(self) -> dict[str, int]:
        """
        sP = P * i / 100 * T / K
        sP - итоговый расчёт
        P - изначальная сумма
        i - годовая процентная ставка
        T - период в течении которого будут начислятся Р
        K - кол-во месяцев в году (12)
        """
        date = self.deposit_date
        result = {}

        P = self.amount
        i = self.rate / 100
        T = self.periods
        K = 12

        for _ in range(T):
            date += timedelta(days=31)
            sP = P + (P * i * T / K)
            result[date.strftime("%d.%m.%Y")] = int(sP)

        return result
