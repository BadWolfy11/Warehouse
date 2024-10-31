from typing import Optional
from pydantic import BaseModel


class AddressBase(BaseModel):
    pass


class AddressCreate(AddressBase):
    city: str
    street: str
    appartament: str


class AddressUpdate(AddressBase):
    city: Optional[str]
    street: Optional[str]
    appartament: Optional[str]


class Address(AddressBase):
    id: Optional[int] = None
    city: str
    street: str
    appartament: str

    class Config:
        from_attributes = True
