from fastapi import Request
from jose import jwt
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def get_current_user_id(request:Request): 
    access_token = request.headers.get("Authorization")
    access_token = access_token.split()[1]
    user_id = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM]).get('id')
    return user_id