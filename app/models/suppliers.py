from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Model


class Supplier(Model):
    __tablename__ = "suppliers"

    idsuppliers: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    business_name: Mapped[str]
    contact_person: Mapped[str]
    phone: Mapped[str] = mapped_column(unique=True)
    supplies = relationship(
        "Supply", back_populates="supplier", cascade="all, delete-orphan"
    )
