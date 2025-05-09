from typing import Optional
from pydantic import BaseModel


class PersonBase(BaseModel):
    pass


class PersonCreate(PersonBase):
    name: str
    last_name: str
    address_id: int
    email: str
    phone: str
    notes: str


class PersonUpdate(PersonBase):
    name: Optional[str]
    last_name: Optional[str]
    address_id: Optional[int]
    email: Optional[str]
    phone: Optional[str]
    notes: Optional[str]


class Person(PersonBase):
    id: int
    name: str
    last_name: str
    address_id: int
    email: str
    phone: str
    notes: str

    class Config:
        from_attributes = True
