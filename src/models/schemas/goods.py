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
    price: float
    stock: int

class GoodsUpdate(GoodsBase):
    barcode: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    attachments: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class Goods(GoodsBase):
    id: int
    barcode: str
    name: str
    description: str
    category_id: int
    attachments: str
    price: float
    stock: int

    class Config:
        from_attributes = True
