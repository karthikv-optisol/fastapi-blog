from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .enums import Gender
from typing import List

from .database import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String,unique=True)
    password = Column(String)
    mobile = Column(Integer)
    gender = Column(Enum(Gender), default=Gender.Male)
    isOnline = Column(Boolean)
