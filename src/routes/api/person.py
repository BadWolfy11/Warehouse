from typing import Optional

from fastapi import APIRouter, Query, Depends
from fastcrud import crud_router

from core.database import get_async_session
from core.models import Person
from models.schemas.person import PersonCreate, PersonUpdate, Person as PersonsSchema
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

crud = crud_router(
    session=get_async_session,
    model=Person,
    create_schema=PersonCreate,
    update_schema=PersonUpdate,
    path="/person",
    tags=["Person"],
)

custom_router = APIRouter(prefix="/person", tags=["Person"])

@custom_router.get("/search", response_model=dict)
async def search_persons(
    id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session),
):
    query = select(Person)
    count_query = select(func.count()).select_from(Person)

    if id is not None:
        query = query.where(Person.id == id)
        count_query = count_query.where(Person.id == id)
    if name is not None:
        query = query.where(Person.name.ilike(f"%{name}%"))
        count_query = count_query.where(Person.name.ilike(f"%{name}%"))
    if last_name is not None:
        query = query.where(Person.last_name.ilike(f"%{last_name}%"))
        count_query = count_query.where(Person.last_name.ilike(f"%{last_name}%"))
    if email is not None:
        query = query.where(Person.email.ilike(f"%{email}%"))
        count_query = count_query.where(Person.email.ilike(f"%{email}%"))
    if phone is not None:
        query = query.where(Person.phone.ilike(f"%{phone}%"))
        count_query = count_query.where(Person.phone.ilike(f"%{phone}%"))

    total_result = await db.execute(count_query)
    total_count = total_result.scalar()

    result = await db.execute(query.offset(offset).limit(limit))
    items = result.scalars().all()

    return {
        "totalCount": total_count,
        "items": [PersonsSchema.from_orm(item) for item in items]
    }

router = APIRouter()
router.include_router(crud)
router.include_router(custom_router)