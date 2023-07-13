from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    pass


class UserOut(BaseModel):
    id: int
    email: str


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime
    id: int
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True
