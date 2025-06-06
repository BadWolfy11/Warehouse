from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastcrud import crud_router
from core.database import get_async_session
from core.models import Categories
from models.schemas.categories import CategoriesCreate, CategoriesUpdate, Categories as CategorySchema

from src.routes.api.expenses import custom_router

# Создаем основной роутер
crud = crud_router(
    session=get_async_session,
    model=Categories,
    create_schema=CategoriesCreate,
    update_schema=CategoriesUpdate,
    path="/categories",
    tags=["Categories"],
)

custom_router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@custom_router.get("/all", response_model=list[CategorySchema], name="Get all categories")
async def get_all_categories(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Categories))
    return result.scalars().all()

router = APIRouter()
router.include_router(crud)
router.include_router(custom_router)
