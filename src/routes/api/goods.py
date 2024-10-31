from fastcrud import crud_router

from core.database import get_async_session
from core.models import Goods
from models.schemas.goods import GoodsCreate, GoodsUpdate

router = crud_router(
    session=get_async_session,
    model=Goods,
    create_schema=GoodsCreate,
    update_schema=GoodsUpdate,
    path="/goods",
    tags=["Goods"],
)
