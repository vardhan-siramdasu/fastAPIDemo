from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserOut(BaseModel):
    email: EmailStr
    createdAt: datetime
    class config:
        orm_mode = True

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    userId: int
    user: UserOut
    #rating:Optional[int] = None
    class config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True

class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    createdAt: datetime

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    userId: int
    postId: int