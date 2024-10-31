from sqlalchemy import Table, Date, Boolean, Text, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Session

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    login = Column(String(50), unique=True ,nullable=False)
    password = Column(String(50),nullable=False)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=True)
    address_id = Column(Integer, ForeignKey('address.id'), nullable=True)
    email = Column(String(9), nullable=False)
    notes = Column(String(255), nullable=False)

class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

class Goods(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    attachments = Column(String(255), nullable=False)

class Documents(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    data = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

class GoodsDocuments(Base):
    __tablename__ = 'goods_documents'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey('goods.id'), nullable=True)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=True)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(255), nullable=False)
    street = Column(String(50), nullable=False)
    appartment = Column(String(255), nullable=False)

class Expenses(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False)
    amount = Column(float, nullable=False)
    name = Column(String(40), nullable=False)
    attachments = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

def get_base():
    return Base