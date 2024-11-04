from fastcrud import crud_router

from core.database import get_async_session
from core.models import Person
from models.schemas.person import PersonCreate, PersonUpdate

router = crud_router(
    session=get_async_session,
    model=Person,
    create_schema=PersonCreate,
    update_schema=PersonUpdate,
    path="/person",
    tags=["Person"],
)
