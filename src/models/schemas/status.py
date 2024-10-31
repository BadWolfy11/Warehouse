from typing import Optional
from pydantic import BaseModel


class StatusBase(BaseModel):
    pass


class StatusCreate(StatusBase):
    name: str


class StatusUpdate(StatusBase):
    name: Optional[str]


class Status(StatusBase):
    id: int


    class Config:
        from_attributes = True

