from fastcrud import crud_router

from core.database import get_async_session
from core.models import Users
from models.schemas.users import UsersCreate, UsersUpdate

router = crud_router(
    session=get_async_session,
    model=Users,
    create_schema=UsersCreate,
    update_schema=UsersUpdate,
    path="/users",
    tags=["Users"],
)
