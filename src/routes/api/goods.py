from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from fastcrud import crud_router
from core.database import get_async_session
from core.models import Goods
from models.schemas.goods import GoodsCreate, GoodsUpdate, Goods as GoodsSchema
from middlewares.authorization import auth_check
from services.history_goods import update_goods_with_history

# основной CRUD-роутер
crud = crud_router(
    session=get_async_session,
    model=Goods,
    create_schema=GoodsCreate,
    update_schema=GoodsUpdate,
    path="/goods",
    tags=["Goods"],
)

#кастомный роутер по поиску товаров
custom_router = APIRouter(
    prefix='/goods',
    tags=['Goods']
)


@custom_router.get("/search", response_model=list[GoodsSchema])
async def search_goods(
    id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    barcode: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_async_session)
):
    query = select(Goods)
    if id is not None:
        query = query.where(Goods.id == id)
    if name is not None:
        query = query.where(Goods.name.ilike(f"%{name}%"))
    if barcode is not None:
        query = query.where(Goods.barcode.ilike(f"%{barcode}%"))
    if category_id is not None:
        query = query.where(Goods.category_id == category_id)

    result = await db.execute(query)
    return result.scalars().all()


@custom_router.put("/{id}", response_model=GoodsSchema)
async def update_goods(
    id: int,
    goods_update: GoodsUpdate,
    user=Depends(auth_check),
    db: AsyncSession = Depends(get_async_session)
):
    return await update_goods_with_history(
        goods_id=id,
        data=goods_update.dict(exclude_unset=True),
        user_id=user.id,
        db=db
    )

router = APIRouter()
router.include_router(crud)
router.include_router(custom_router)
