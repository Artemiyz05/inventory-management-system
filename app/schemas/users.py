from pydantic import BaseModel


class SUserBase(BaseModel):
    username: str
    password: str


class SUserAdd(SUserBase):
    full_name: str
    type_id: int


class SupplierUpdate(BaseModel):
    business_name: str
    contact_person: str
    phone: str
