from pydantic import BaseModel
from typing import Optional

class AuthBase(BaseModel):
    pass


class AuthLogin(AuthBase):
    login: str
    password: str


class AuthRegistration(AuthBase):
    login: str
    password: str
    password_confirm: str


class AuthSuccess(AuthBase):
    user_id: Optional[int]
    person_id: Optional[int]
    role_id: Optional[int]
    login: str
    access_token: str



