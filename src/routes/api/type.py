from fastcrud import crud_router

from core.database import get_async_session
from core.models import Type
from models.schemas.type import TypeCreate, TypeUpdate

router = crud_router(
    session=get_async_session,
    model=Type,
    create_schema=TypeCreate,
    update_schema=TypeUpdate,
    path="/type",
    tags=["Type"],
)
