from pydantic import BaseModel


class FollowRequestSchema(BaseModel):
    follow_id: int

    class Config:
        from_attributes = True
