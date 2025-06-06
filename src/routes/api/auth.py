from fastapi import APIRouter, HTTPException, Depends
from fastcrud import FastCRUD
from core.database import get_async_session
from core.models import Users, Role
from core.config import settings
from models.schemas.users import UsersCreate

from jose import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from models.schemas.auth import (
    AuthSuccess,
    AuthLogin,
    AuthRegistration
)

router = APIRouter(prefix="/auth", tags=["Auth"])
#Использование шифрования при создании и проверки пароля
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
crud_user = FastCRUD(Users)
crud_role = FastCRUD(Role)
#Роут авторизации пользователя
@router.post(
    "/login",
    response_model=AuthSuccess,
    name="User authorization"
)
async def login(data: AuthLogin, con = Depends(get_async_session)) -> AuthSuccess:
    error = HTTPException(status_code=401, detail="Bad credentials")

    if not len(data.login) or not len(data.password):
        raise error
    #Поиск пользователя в базе данных
    user = await crud_user.get(db=con, login=data.login)

    try:
        if user is None or not pwd_context.verify(data.password, user['password']):
            raise error
    except UnknownHashError:
        raise error

    role = None

    if user['role_id'] is not None:
        role = await crud_role.get(db=con, id=user['role_id'])
    #Возвращаемые данные при успешной авторизации
    return AuthSuccess(
        user_id=user['id'],
        person_id=user['person_id'],
        role_id=user['role_id'],
        login=user['login'],
        access_token=await create_access_token(
            id=user['id'],
            person_id=user['person_id'],
            role_id=user['role_id'],
        )
    )

#Метод создания токена при успешной авторизации или регистрации
async def create_access_token(id: int, person_id: int | None, role_id: int | None):
    return jwt.encode(
        {
            "sub": str(id),
            "person_id": person_id,
            "role_id": role_id,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_LIFETIME_MINUTES)
        },
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

@router.post(
    "/registration",
    response_model=AuthSuccess,
    name="User registration"
)
async def registration(data: AuthRegistration, con = Depends(get_async_session)) -> AuthSuccess:
    if data.password != data.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords not matches")

    find_user = await crud_user.get(db=con, login=data.login)

    if find_user is not None:
        raise HTTPException(status_code=400, detail="User exists")

    role = await crud_role.get(db=con, id=data.role_id)

    if role is None:
        raise HTTPException(status_code=400, detail="Invalid role_id")

    create = await crud_user.create(
        db=con,
        object=UsersCreate(
            person_id=data.person_id,
            role_id=role['id'],
            login=data.login,
            password=pwd_context.hash(data.password)
        ),
    )

    return AuthSuccess(
        user_id=create.id,
        person_id=None,
        login=data.login,
        access_token=await create_access_token(
            id=create.id,
            person_id=-1,
            role_id=role['id'] if role else None
        ),
        role_id=role['id'] if role else None
    )
