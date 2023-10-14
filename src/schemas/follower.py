from datetime import datetime

from pydantic import BaseModel


class FollowRequestSchema(BaseModel):
    follow_id: int

    class Config:
        from_attributes = True


class FShcema(BaseModel):
    id: int
    request: str
    follow_by_id: int
    follow_id: int

    class Config:
        from_attributes = True


class UserSchemaFollower(BaseModel):
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
