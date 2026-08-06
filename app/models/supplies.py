from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.database import Model

from datetime import date


class Supply(Model):
    __tablename__ = "supplies"

    idsupplies: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.idsuppliers"), index=True
    )
    detail_id: Mapped[int] = mapped_column(ForeignKey("details.iddetails"), index=True)
    quantity: Mapped[int]
    date: Mapped[date]

    supplier = relationship("Supplier", back_populates="supplies")
    detail = relationship("Detail", back_populates="supplies")
