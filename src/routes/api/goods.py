from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from core.models import GoodsHistory
from models.schemas.goods_history import GoodsHistoryOut
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


@custom_router.patch("/{id}", response_model=GoodsSchema)
async def update_goods(
    id: int,
    goods_update: GoodsUpdate,
    user=Depends(auth_check),
    db: AsyncSession = Depends(get_async_session)
):
    return await update_goods_with_history(
        goods_id=id,
        data=goods_update.dict(exclude_unset=True),
        user_id=user["id"],
        db=db
    )

custom_rout = APIRouter(prefix="/goods_history", tags=["GoodsHistory"])

@custom_rout.get("/search", response_model=dict)
async def search_goods_history(
    goods_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    field_changed: Optional[str] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
):
    query = select(GoodsHistory)
    count_query = select(func.count()).select_from(GoodsHistory)

    if goods_id is not None:
        query = query.where(GoodsHistory.goods_id == goods_id)
        count_query = count_query.where(GoodsHistory.goods_id == goods_id)
    if user_id is not None:
        query = query.where(GoodsHistory.user_id == user_id)
        count_query = count_query.where(GoodsHistory.user_id == user_id)
    if action is not None:
        query = query.where(GoodsHistory.action.ilike(f"%{action}%"))
        count_query = count_query.where(GoodsHistory.action.ilike(f"%{action}%"))
    if field_changed is not None:
        query = query.where(GoodsHistory.field_changed.ilike(f"%{field_changed}%"))
        count_query = count_query.where(GoodsHistory.field_changed.ilike(f"%{field_changed}%"))

    total_result = await db.execute(count_query)
    total_count = total_result.scalar()

    result = await db.execute(query.order_by(GoodsHistory.changed_at.desc()).offset(offset).limit(limit))
    items = result.scalars().all()

    return {
        "totalCount": total_count,
        "items": [GoodsHistoryOut.from_orm(item) for item in items]
    }

router = APIRouter()
router.include_router(custom_router)
router.include_router(crud)
router.include_router(custom_rout)

