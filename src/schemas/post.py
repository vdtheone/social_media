from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel


class PostCreateSchema(BaseModel):
    location :str
    caption :str

    class Config:
        from_attributes = True


class PostSchema(BaseModel):
    id : int
    location : str
    caption : str
    image : str
    number_of_likes : int
    number_of_comments : int
    user_id : int
    created_at : datetime
    updated_at : datetime

    class Config:
        from_attributes = True


class PostWithUser(BaseModel):
    username:str
    post:PostSchema


class PostWithUser_(PostSchema):
    username:str