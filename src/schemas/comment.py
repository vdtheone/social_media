from datetime import datetime
from pydantic import BaseModel


class CommentSchema(BaseModel):
    desc : str
    # user_id : str
    # post_id : str

    class Config:
        from_attributes = True