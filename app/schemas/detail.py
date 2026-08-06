from pydantic import BaseModel, Field
from decimal import Decimal


class DetailUpdate(BaseModel):
    name: str = Field(min_length=1)
    article: str = Field(min_length=1)
    price: Decimal = Field(ge=0)
    note: str | None = None
