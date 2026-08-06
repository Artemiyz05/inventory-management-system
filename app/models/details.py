from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Model
from decimal import Decimal


class Detail(Model):
    __tablename__ = "details"

    iddetails: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    name: Mapped[str]
    article: Mapped[str] = mapped_column(unique=True)
    price: Mapped[Decimal]
    note: Mapped[str | None] = mapped_column(nullable=True)
    supplies = relationship("Supply", back_populates="detail")
