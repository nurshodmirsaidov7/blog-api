from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    content: str
    image: str | None = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    image: str | None = None
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    author_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True
