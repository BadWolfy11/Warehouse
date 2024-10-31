from typing import Optional
from pydantic import BaseModel


class CategoriesBase(BaseModel):
    pass


class CategoriesCreate(CategoriesBase):
    name: str



class CategoriesUpdate(CategoriesBase):
    name: Optional[str]


class Categories(CategoriesBase):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True
