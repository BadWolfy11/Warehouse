from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GoodsHistoryBase(BaseModel):
    goods_id: int
    user_id: int
    action: str
    field_changed: str
    old_value: Optional[str]
    new_value: Optional[str]
    changed_at: datetime

class GoodsHistoryOut(GoodsHistoryBase):
    id: int


    class Config:
        from_attributes = True
