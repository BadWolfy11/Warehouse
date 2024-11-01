from typing import Optional
from pydantic import BaseModel


class ExpensesBase(BaseModel):
    pass


class ExpensesCreate(ExpensesBase):
    data: int
    amount: int
    name: str
    attachments: str
    category_id: int


class ExpensesUpdate(ExpensesBase):
    data: Optional[date]
    amount: Optional[int]
    name: Optional[str]
    attachments: Optional[str]
    user_id: Optional[int]


class Expenses(ExpensesBase):
    id: int
    data: int
    amount: int
    name: str
    attachments: str
    category_id: int

    class Config:
        from_attributes = True

