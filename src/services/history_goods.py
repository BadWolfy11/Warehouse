from core.models import Goods
from models.schemas.goods_history import GoodsHistoryBase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from datetime import datetime

from src.core.models import GoodsHistory


async def update_goods_with_history(goods_id: int, data: dict, user_id: int, db: AsyncSession):
    goods = await db.get(Goods, goods_id)
    if not goods:
        raise HTTPException(status_code=404, detail="Товар не найден")

    fields_to_track = ['price', 'stock', 'name', 'description', 'attachments']
    history = []

    for field in fields_to_track:
        if field in data:
            old_value = getattr(goods, field)
            new_value = data[field]
            if str(old_value) != str(new_value):
                history.append(GoodsHistory(
                    goods_id=goods_id,
                    user_id=user_id,
                    action="update",
                    field_changed=field,
                    old_value=str(old_value),
                    new_value=str(new_value),
                    changed_at=datetime.utcnow()
                ))
                setattr(goods, field, new_value)

    db.add_all(history)
    await db.commit()
    await db.refresh(goods)

    return goods
