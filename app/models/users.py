from sqlalchemy.orm import Mapped, mapped_column
from app.database import Model


class User(Model):
    __tablename__ = "users"

    iduser: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    full_name: Mapped[str]
    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    typeid: Mapped[int]
    email: Mapped[str | None] = mapped_column(nullable=True, default=None)
