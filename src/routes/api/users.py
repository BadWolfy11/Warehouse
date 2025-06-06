from fastcrud import crud_router


from models.schemas.users import UsersCreate, UsersUpdate

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.database import get_async_session
from core.models import Users
from models.schemas.users import Users as UsersSchema

crud = crud_router(
    session=get_async_session,
    model=Users,
    create_schema=UsersCreate,
    update_schema=UsersUpdate,
    path="/users",
    tags=["Users"],
)

custom_router = APIRouter(prefix="/users", tags=["Users"])

@custom_router.get("/search", response_model=dict)
async def search_users(
    id: Optional[int] = Query(None),
    login: Optional[str] = Query(None),
    person_id: Optional[int] = Query(None),
    role_id: Optional[int] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
):
    query = select(Users)
    count_query = select(func.count()).select_from(Users)

    if id is not None:
        query = query.where(Users.id == id)
        count_query = count_query.where(Users.id == id)
    if login is not None:
        query = query.where(Users.login.ilike(f"%{login}%"))
        count_query = count_query.where(Users.login.ilike(f"%{login}%"))
    if person_id is not None:
        query = query.where(Users.person_id == person_id)
        count_query = count_query.where(Users.person_id == person_id)
    if role_id is not None:
        query = query.where(Users.role_id == role_id)
        count_query = count_query.where(Users.role_id == role_id)

    total_result = await db.execute(count_query)
    total_count = total_result.scalar()

    result = await db.execute(query.offset(offset).limit(limit))
    items = result.scalars().all()

    return {
        "totalCount": total_count,
        "items": [UsersSchema.from_orm(item) for item in items]
    }

router = APIRouter()
router.include_router(crud)           # от fastcrud
router.include_router(custom_router)  # наш кастомный поиск
