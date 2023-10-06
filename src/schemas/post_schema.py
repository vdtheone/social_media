from datetime import datetime
from pydantic import BaseModel


class PostSchema(BaseModel):
    location :str
    caption : str
    upload_time : datetime
    number_of_likes : int
    number_of_comments : int

    class Config:
        from_attributes = True