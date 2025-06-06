from typing import Optional
from pydantic import BaseModel


class AddressBase(BaseModel):
    pass


class AddressCreate(AddressBase):
    city: str
    street: str
    appartment: str


class AddressUpdate(AddressBase):
    city: Optional[str]
    street: Optional[str]
    appartment: Optional[str]


class Address(AddressBase):
    id: Optional[int] = None
    city: str
    street: str
    appartment: str

    class Config:
        from_attributes = True
