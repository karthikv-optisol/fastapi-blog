from pydantic import BaseModel  # type: ignore
from .enums import Gender
from typing import Optional
from typing import List


class Blog(BaseModel):
    title: str
    body: str


class showBlog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str
    mobile: str
    gender: Optional[Gender]
    isOnline: bool

    class Config:
        orm_mode = True


class showUser(BaseModel):
    id: int
    name: str
    email: str
    mobile: int
    gender: str

    class Config:
        orm_mode = True

class loginUser(BaseModel):
    email:str
    password:str
    
    class Config:
        orm_mode = True