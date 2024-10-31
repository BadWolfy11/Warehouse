from fastcrud import crud_router

from core.database import get_async_session
from core.models import Categories
from models.schemas.categories import CategoriesCreate, CategoriesUpdate

router = crud_router(
    session=get_async_session,
    model=Categories,
    create_schema=CategoriesCreate,
    update_schema=CategoriesUpdate,
    path="/categories",
    tags=["Categories"],
)
