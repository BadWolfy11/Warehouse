from typing import Optional
from pydantic import BaseModel


class UsersBase(BaseModel):
    pass


class UsersCreate(UsersBase):
    name: str
    last_name: str
    login: str
    password: str
    status_id: int
    address_is: int
    email: str
    notes: str


class UsersUpdate(UsersBase):
    name: Optional[str]
    last_name: Optional[str]
    login: Optional[str]
    password: Optional[str]
    status_id: Optional[int]
    address_is: Optional[int]
    email: Optional[str]
    notes: Optional[str]


class Users(UsersBase):
    id: int
    name: str
    last_name: str
    login: str
    password: str
    status_id: int
    address_is: int
    email: str
    notes: str

    class Config:
        from_attributes = True
