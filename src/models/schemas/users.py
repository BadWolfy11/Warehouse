from typing import Optional
from pydantic import BaseModel

class UsersCreate(BaseModel):
    person_id: Optional[int] = None
    role_id: Optional[int] = None
    login: str
    password: str

class UsersBase(UsersCreate):
    id: Optional[int] = None

class UsersFind(UsersBase):
    person_id: Optional[int]
    role_id: Optional[int]
    login: Optional[str]


class UsersUpdate(UsersBase):
    person_id: Optional[int]
    login: Optional[str]
    password: Optional[str]
    person_id: Optional[int]
    role_id: Optional[int]


class Users(UsersBase):
    person_id: int
    role_id: int
    login: str
    password: str

    class Config:
        from_attributes = True