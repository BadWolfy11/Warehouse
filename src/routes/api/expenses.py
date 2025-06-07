from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import date
from sqlalchemy import func

from fastcrud import crud_router
from core.database import get_async_session
from core.models import Expenses
from models.schemas.expenses import ExpensesCreate, ExpensesUpdate, Expenses as ExpensesSchema


crud = crud_router(
    session=get_async_session,
    model=Expenses,
    create_schema=ExpensesCreate,
    update_schema=ExpensesUpdate,
    path="/expenses",
    tags=["Expenses"],
)


custom_router = APIRouter(
    prefix='/expenses',
    tags=["Expenses"]
)


@custom_router.get("/search", response_model=dict)
async def search_expenses(
    id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    expense_category_id: Optional[int] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
):
    query = select(Expenses)
    count_query = select(func.count()).select_from(Expenses)

    if id is not None:
        query = query.where(Expenses.id == id)
        count_query = count_query.where(Expenses.id == id)
    if name is not None:
        query = query.where(Expenses.name.ilike(f"%{name}%"))
        count_query = count_query.where(Expenses.name.ilike(f"%{name}%"))
    if expense_category_id is not None:
        query = query.where(Expenses.expense_category_id == expense_category_id)
        count_query = count_query.where(Expenses.expense_category_id == expense_category_id)

    total_result = await db.execute(count_query)
    total_count = total_result.scalar()

    result = await db.execute(query.offset(offset).limit(limit))
    items = result.scalars().all()

    return {
        "totalCount": total_count,
        "items": [ExpensesSchema.from_orm(item) for item in items]
    }


router = APIRouter()
router.include_router(crud)
router.include_router(custom_router)
