from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel


class PostSchema(BaseModel):
    location :str
    caption :str
    # number_of_likes :int
    # number_of_comments :int
    

    class Config:
        from_attributes = True