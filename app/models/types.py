from sqlalchemy.orm import Mapped, mapped_column
from app.database import Model


class Type(Model):
    __tablename__ = "types"

    idtype: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    type: Mapped[str] = mapped_column(unique=True, index=True)
