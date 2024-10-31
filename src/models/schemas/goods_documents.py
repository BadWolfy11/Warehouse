from typing import Optional
from pydantic import BaseModel


class GoodsDocumentsBase(BaseModel):
    pass


class GoodsDocumentsCreate(GoodsDocumentsBase):
    name: str
    quantity: int
    item_id: int
    document_id: int


class GoodsDocumentsUpdate(GoodsDocumentsBase):
    name: Optional[str]
    quantity: Optional[int]
    item_id: Optional[int]
    document_id:Optional[int]



class GoodsDocuments(GoodsDocumentsBase):
    id: int
    name: str
    quantity: int
    item_id: int
    document_id: int

    class Config:
        from_attributes = True
