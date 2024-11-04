from typing import Optional
from pydantic import BaseModel


class TypeBase(BaseModel):
    pass


class TypeCreate(TypeBase):
    name: str


class TypeUpdate(TypeBase):
    name: Optional[str]


class Type(TypeBase):
    id: int


    class Config:
        from_attributes = True

