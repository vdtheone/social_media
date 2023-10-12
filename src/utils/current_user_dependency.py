import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.config import SessionLocal
from src.models.user import User

ALGORITHM = os.environ.get("ALGORITHM")
SECRET_KEY = os.environ.get("SECRET_KEY")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)
):
    try:
        # print(token)
        # token = token.split()[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token not provided",
                headers={"WWW-Authenticate": "Bearer"},
            )
        id = payload.get("id")
        if id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not get valid key(id)",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(User).get(id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expired")
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
