from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastcrud import FastCRUD
from core.database import get_async_session
from core.models import Users
from jose import JWTError, jwt
from core.config import settings
from models.schemas.users import Users as UsersBase

security = HTTPBearer()
crud_user = FastCRUD(Users)

#проверка токена для действий с API
async def auth_check(token: Annotated[str, Depends(security)], con = Depends(get_async_session)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    user_id: str | None = None

    try:
        payload = jwt.decode(token.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    user = await crud_user.get(db=con, schema_to_select=UsersBase, id=int(user_id))

    if user is None:
        raise credentials_exception

    return user
