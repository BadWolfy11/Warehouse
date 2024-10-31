from fastcrud import crud_router

from core.database import get_async_session
from core.models import Expenses
from models.schemas.expenses import ExpensesCreate, ExpensesUpdate

router = crud_router(
    session=get_async_session,
    model=Expenses,
    create_schema=ExpensesCreate,
    update_schema=ExpensesUpdate,
    path="/expenses",
    tags=["Expenses"],
)
