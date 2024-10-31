from typing import Optional
from pydantic import BaseModel


class GoodsBase(BaseModel):
    pass


class GoodsCreate(GoodsBase):
    barcode: str
    name: str
    description: str
    category_id: int
    attachments: str



class GoodsUpdate(GoodsBase):
    barcode: Optional[str]
    name: Optional[str]
    description: Optional[str]
    category_id: Optional[int]
    attachments: Optional[str]


class Goods(GoodsBase):
    id: int
    barcode: str
    name: str
    description: str
    category_id: int
    attachments: str

    class Config:
        from_attributes = True

