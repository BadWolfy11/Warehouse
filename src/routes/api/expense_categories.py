
from fastcrud import crud_router
from fastapi import APIRouter, Depends

from sqlalchemy import select

from core.database import get_async_session
from core.models import ExpenseCategories
from models.schemas.expense_categories import ExpenseCategoriesCreate, ExpenseCategoriesUpdate, ExpenseCategories as ExpenseCategorySchema
from sqlalchemy.ext.asyncio import AsyncSession

crud = crud_router(
    session=get_async_session,
    model=ExpenseCategories,
    create_schema=ExpenseCategoriesCreate,
    update_schema=ExpenseCategoriesUpdate,
    path="/expense_categories",
    tags=["ExpenseCategories"],
)
expense_categories_router = APIRouter(
    prefix="/expense_categories",
    tags=["Expense Categories"],
)

@expense_categories_router.get(
    "/all",
    response_model=list[ExpenseCategorySchema],
    name="Получить все категории расходов"
)
async def get_all_expense_categories(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(ExpenseCategories))
    return result.scalars().all()


router = APIRouter()
router.include_router(crud)
router.include_router(expense_categories_router)
