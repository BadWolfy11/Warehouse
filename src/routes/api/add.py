from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_async_session
from core.models import Address, Person, Users
from models.schemas.users import UsersCreate, Users
from models.schemas.person import PersonCreate
from models.schemas.address import AddressCreate
from models.schemas.role import Role
from fastapi import status

router = APIRouter()

@router.post("/user/full-create", response_model=Users, status_code=status.HTTP_201_CREATED)
async def full_create_user(
    user_data: UsersCreate,  # логин, пароль, role_id
    person_data: PersonCreate,  # имя, фамилия, email, phone, address_id (временно None)
    address_data: AddressCreate,  # city, street, appartment
    db: AsyncSession = Depends(get_async_session)
):
    # 1. Создание или поиск адреса
    addr_query = select(Address).where(
        Address.city == address_data.city,
        Address.street == address_data.street,
        Address.appartment == address_data.appartment
    )
    address = (await db.execute(addr_query)).scalars().first()
    if not address:
        address = Address(**address_data.dict())
        db.add(address)
        await db.flush()
        await db.refresh(address)

    # 2. Создание или поиск персоны
    person_query = select(Person).where(
        Person.name == person_data.name,
        Person.last_name == person_data.last_name,
        Person.email == person_data.email,
        Person.phone == person_data.phone
    )
    person = (await db.execute(person_query)).scalars().first()
    if not person:
        person = Person(**person_data.dict(), address_id=address.id)
        db.add(person)
        await db.flush()
        await db.refresh(person)

    # 3. Проверка на уникальность логина
    existing_user = await db.execute(select(Users).where(Users.login == user_data.login))
    if existing_user.scalars().first():
        raise HTTPException(status_code=409, detail="Пользователь с таким логином уже существует")

    # 4. Создание пользователя
    new_user = Users(
        login=user_data.login,
        password=user_data.password,
        role_id=user_data.role_id,
        person_id=person.id
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
