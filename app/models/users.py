from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.database import Model


class User(Model):
    __tablename__ = "users"

    iduser: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    full_name: Mapped[str]
    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    type_id: Mapped[int] = mapped_column(ForeignKey("types.idtype"))
    email: Mapped[str | None] = mapped_column(unique=True, nullable=True, default=None)
