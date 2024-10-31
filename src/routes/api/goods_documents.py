from fastcrud import crud_router

from core.database import get_async_session
from core.models import GoodsDocuments
from models.schemas.goods_documents import GoodsDocumentsCreate, GoodsDocumentsUpdate

router = crud_router(
    session=get_async_session,
    model=GoodsDocuments,
    create_schema=GoodsDocumentsCreate,
    update_schema=GoodsDocumentsUpdate,
    path="/goods_documents",
    tags=["GoodsDocuments"],
)
