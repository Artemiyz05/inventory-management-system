from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.database import Model

from decimal import Decimal
from datetime import date


class History_price(Model):
    __tablename__ = "history_prices"

    idhistory_price: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    price: Mapped[Decimal]
    date: Mapped[date]
    detail_id: Mapped[int] = mapped_column(ForeignKey("details.iddetails"), index=True)
