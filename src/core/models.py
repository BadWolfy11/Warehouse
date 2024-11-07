from sqlalchemy import Table, Date, Boolean, Text, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy import Column, Integer, String, ForeignKey, Double
from sqlalchemy.orm import DeclarativeBase, relationship, Session

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True ,nullable=False)
    password = Column(String(50), nullable=False)
    role_id = Column(Integer, ForeignKey('status.id'), nullable=True)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=True)

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'), nullable=True)
    email = Column(String(100), nullable=False)
    phone = Column(String(9), nullable=False)
    notes = Column(String(255), nullable=False)

class Role(Base):
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
    type_id = Column(Integer, ForeignKey('type.id'), nullable=True)
    name = Column(String(255), nullable=False)
    data = Column(Date, nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=True)

class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

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
    amount = Column(Integer, nullable=False)
    name = Column(String(40), nullable=False)
    attachments = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

def get_base():
    return Base