from collections.abc import AsyncGenerator, Callable
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from typing import Any
from loguru import logger
import asyncio

import fastapi
from fastapi import APIRouter, FastAPI, Depends
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from fastcrud import FastCRUD
from .config import Settings
from .models import get_base, Users, Role
from models.schemas.users import UsersCreate
from models.schemas.role import RoleCreate
from .database import async_engine as engine, get_async_session
from passlib.context import CryptContext

crud_user = FastCRUD(Users)
crud_role = FastCRUD(Role)
settings = Settings()

async def create_tables() -> None:
    async with engine.begin() as conn:
        logger.info("Создание базы")
        Base = get_base()
        await conn.run_sync(Base.metadata.create_all)


async def check_roles(conn = get_async_session()):
    logger.info("Проверка существования ролей")
    conn = await anext(conn)

    if not await crud_role.get(db=conn, code=settings.APP_EMPLOYER_DEFAULT_ROLE_CODE):
        await crud_role.create(db=conn, object=RoleCreate(
            name="Товаровед",
            code=settings.APP_EMPLOYER_DEFAULT_ROLE_CODE,
            access=50
        ))

    if not await crud_role.get(db=conn, code=settings.APP_ADMIN_DEFAULT_ROLE_CODE):
        await crud_role.create(db=conn, object=RoleCreate(
            name="Администратор",
            code=settings.APP_ADMIN_DEFAULT_ROLE_CODE,
            access=100
        ))


async def check_admin_user(conn = get_async_session()) -> None:
    logger.info("Проверка существования администратора")
    conn = await anext(conn)

    if not await crud_user.get(db=conn, login=settings.ADMIN_USERNAME):
        admin_role = await crud_role.get(db=conn, code=settings.APP_ADMIN_DEFAULT_ROLE_CODE)
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        await crud_user.create(
            db=conn,
            object=UserCreate(
                person_id=None,
                role_id=admin_role['id'],
                login=settings.ADMIN_USERNAME,
                password=pwd_context.hash(settings.ADMIN_PASSWORD)
            )
        )


def lifespan_factory(settings: Settings) -> Callable[[FastAPI], _AsyncGeneratorContextManager[Any]]:
    logger.info("Lifespan entry")

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:
        await create_tables()

        if settings.APP_GENERATE_FIRST_USER_AND_ROLES:
            await check_roles()
            await check_admin_user()
        yield

    return lifespan


def create_application(
    router: APIRouter,
    settings: Settings,
    **kwargs: Any,
) -> FastAPI:
    logger.info("создание приложения")

    logger.info("Configure app settings..")
    kwargs.update({
        "title": settings.APP_NAME,
        "description": settings.APP_DESCRIPTION,
        "contact": {"name": settings.APP_CONTACT_NAME, "email": settings.APP_CONTACT_EMAIL},
        "license_info": {"name": settings.APP_LICENSE_NAME}
    })

    lifespan = lifespan_factory(settings=settings)

    logger.info("Init FastAPI..")
    application = FastAPI(lifespan=lifespan, **kwargs)
    application.include_router(router)


    logger.info("Приложение успешно создано")
    return application