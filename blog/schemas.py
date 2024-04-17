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
        # orm_mode=True - old version
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str
    mobile: str
    gender: Optional[Gender]
    is_online: bool
    class Config:
        orm_mode = True
        
