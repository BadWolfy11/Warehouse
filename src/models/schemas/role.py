from typing import Optional
from pydantic import BaseModel


class RoleBase(BaseModel):
    pass


class RoleCreate(RoleBase):
    name: str


class RoleUpdate(RoleBase):
    name: Optional[str]


class Role(RoleBase):
    id: int
    name: str


    class Config:
        from_attributes = True

