from fastcrud import crud_router

from core.database import get_async_session
from core.models import Role
from models.schemas.role import RoleCreate, RoleUpdate

router = crud_router(
    session=get_async_session,
    model=Role,
    create_schema=RoleCreate,
    update_schema=RoleUpdate,
    path="/role",
    tags=["Role"],
)
