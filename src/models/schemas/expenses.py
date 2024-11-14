from typing import Optional
from pydantic import BaseModel
from datetime import date


class ExpensesBase(BaseModel):
    pass


class ExpensesCreate(ExpensesBase):
    data: date
    amount: int
    name: str
    attachments: str
    expense_category_id: int


class ExpensesUpdate(ExpensesBase):
    data: Optional[date]
    amount: Optional[int]
    name: Optional[str]
    attachments: Optional[str]
    expense_category_id: Optional[int]


class Expenses(ExpensesBase):
    id: int
    data: date
    amount: int
    name: str
    attachments: str
    expense_category_id: int

    class Config:
        from_attributes = True

