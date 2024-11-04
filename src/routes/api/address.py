from fastcrud import crud_router

from core.database import get_async_session
from core.models import Address
from models.schemas.address import AddressCreate, AddressUpdate

router = crud_router(
    session=get_async_session,
    model=Address,
    create_schema=AddressCreate,
    update_schema=AddressUpdate,
    path="/address",
    tags=["Address"],
)
