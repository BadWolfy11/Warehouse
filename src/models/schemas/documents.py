# from typing import Optional
# from pydantic import BaseModel
# from datetime import date
#
#
# class DocumentsBase(BaseModel):
#     pass
#
#
# class DocumentsCreate(DocumentsBase):
#     type_id: int
#     name: str
#     data: date
#     person_id: int
#
#
# class DocumentsUpdate(DocumentsBase):
#     type_id: Optional[int]
#     name: Optional[str]
#     data: Optional[date]
#     person_id: Optional[int]
#
#
# class Documents(DocumentsBase):
#     type_id: int
#     id: int
#     name: str
#     data: date
#     person_id: int
#
#     class Config:
#         from_attributes = True
#
