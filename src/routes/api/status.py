from fastcrud import crud_router

from core.database import get_async_session
from core.models import Status
from models.schemas.status import StatusCreate, StatusUpdate

router = crud_router(
    session=get_async_session,
    model=Status,
    create_schema=StatusCreate,
    update_schema=StatusUpdate,
    path="/status",
    tags=["Status"],
)
