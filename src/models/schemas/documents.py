from typing import Optional
from pydantic import BaseModel


class DocumentsBase(BaseModel):
    pass


class DocumentsCreate(DocumentsBase):
    name: str
    data: date
    user_id: int


class DocumentsUpdate(DocumentsBase):
    name: Optional[str]
    data: Optional[date]
    user_id: Optional[int]


class Documents(DocumentsBase):
    id: int
    name: str
    data: date
    user_id: int

    class Config:
        from_attributes = True

