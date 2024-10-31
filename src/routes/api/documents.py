from fastcrud import crud_router

from core.database import get_async_session
from core.models import Documents
from models.schemas.documents import DocumentsCreate, DocumentsUpdate

router = crud_router(
    session=get_async_session,
    model=Documents,
    create_schema=DocumentsCreate,
    update_schema=DocumentsUpdate,
    path="/documents",
    tags=["Documents"],
)
