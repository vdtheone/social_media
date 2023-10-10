from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.schemas.post import PostSchema


class GetUser(BaseModel):
    first_name: str
    last_name: str
    mobile_no: int
    username: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_deleted: bool

    class Config:
        from_attributes = True


class CreateUserSchema(GetUser):
    password: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class UserWithPosts(GetUser):
    posts: List[PostSchema]


class UpdateUser(BaseModel):
    first_name: str
    last_name: str
    mobile_no: int
    username: str
    password: str
