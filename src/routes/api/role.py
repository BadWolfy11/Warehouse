from fastapi import APIRouter, Depends
from fastcrud import crud_router
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session
from core.models import Role as RoleModel  # SQLAlchemy-модель
from models.schemas.role import RoleCreate, RoleUpdate, Role  # Pydantic-схемы


crud = crud_router(
    session=get_async_session,
    model=RoleModel,
    create_schema=RoleCreate,
    update_schema=RoleUpdate,
    path="/role",
    tags=["Role"],
)


custom_router = APIRouter(
    prefix="/role",
    tags=["Role"],
)

@custom_router.get("/all", response_model=list[Role])
async def get_all_roles(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(RoleModel))
    return result.scalars().all()


# Финальный роутер
router = APIRouter()
router.include_router(crud)
router.include_router(custom_router)
