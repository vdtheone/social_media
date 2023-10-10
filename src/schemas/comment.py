from pydantic import BaseModel


class CommentSchema(BaseModel):
    desc: str

    class Config:
        from_attributes = True
