from typing import Optional
from pydantic import BaseModel


class ExpenseCategoriesBase(BaseModel):
    pass


class ExpenseCategoriesCreate(ExpenseCategoriesBase):
    name: str



class ExpenseCategoriesUpdate(ExpenseCategoriesBase):
    name: Optional[str]


class ExpenseCategories(ExpenseCategoriesBase):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True
