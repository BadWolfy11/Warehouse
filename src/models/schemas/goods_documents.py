from typing import Optional
from pydantic import BaseModel


class GoodsDocumentsCreate(BaseModel):
    quantity: int
    item_id: int
    document_id: int


class GoodsDocumentsUpdate(BaseModel):
    quantity: Optional[int]
    item_id: Optional[int]
    document_id:Optional[int]


class GoodsDocuments(BaseModel):
    id: int
    quantity: int
    item_id: int
    document_id: int

    class Config:
        from_attributes = True

class GoodsDump(BaseModel):
    documents: list
    total: int
