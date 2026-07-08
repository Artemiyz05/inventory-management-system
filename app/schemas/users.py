from pydantic import BaseModel


class SUserBase(BaseModel):
    username: str
    password: str


class SUserAdd(SUserBase):
    full_name: str
    typeid: int
