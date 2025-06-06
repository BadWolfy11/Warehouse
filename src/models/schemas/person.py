from typing import Optional
from pydantic import BaseModel


class PersonBase(BaseModel):
    name: str
    last_name: str
    address_id: int
    email: str
    phone: str


class PersonCreate(PersonBase): # Можно сразу на запросах юзать PersonBase, если делаешь роуты не через круд
    pass


class PersonUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    address_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class Person(PersonBase):
    id: int

    class Config:
        from_attributes = True
