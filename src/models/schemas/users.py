from typing import Optional
from pydantic import BaseModel


class UsersBase(BaseModel):
    person_id: Optional[int] = None
    role_id: Optional[int] = None
    login: str
    password: str


class UsersCreate(UsersBase):
    pass


class UsersUpdate(BaseModel):
    login: Optional[str] = None
    password: Optional[str] = None
    person_id: Optional[int] = None
    role_id: Optional[int] = None


class Users(UsersBase):
    id: int

    class Config:
        from_attributes = True

