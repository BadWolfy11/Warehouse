from fastcrud import crud_router

from core.database import get_async_session
from core.models import ExpenseCategories
from models.schemas.expense_categories import ExpenseCategoriesCreate, ExpenseCategoriesUpdate

router = crud_router(
    session=get_async_session,
    model=ExpenseCategories,
    create_schema=ExpenseCategoriesCreate,
    update_schema=ExpenseCategoriesUpdate,
    path="/expense_categories",
    tags=["ExpenseCategories"],
)
