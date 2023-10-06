from datetime import datetime
from pydantic import BaseModel


class GetAllUser(BaseModel):
    first_name :str
    last_name  :str
    mobile_no  :int
    username  :str
    created_at: datetime
    updated_at: datetime
    is_active : bool
    is_deleted : bool

    class Config:
        from_attributes = True


class CreateUserSchema(GetAllUser):
    password  :str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username:str
    password:str

    class Config:
        from_attributes = True