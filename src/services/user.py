from fastapi import HTTPException, Request, status
from src.schemas.user import UserLogin, CreateUserSchema
from src.models.user import User
from sqlalchemy.orm import Session

from src.utils.required_jwt import access_token_required
from src.utils.generate_jwt_token import (
    create_jwt_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)


def create_user_new(request: Request, user: CreateUserSchema, db: Session):
    user_exists = db.query(User).filter(User.username == user.username).first()

    if user_exists:
        raise HTTPException(status_code=403, detail="User Already Exists")

    create_new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        mobile_no=user.mobile_no,
        username=user.username,
        password=get_hashed_password(user.password),
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
    db.add(create_new_user)
    db.commit()
    db.refresh(create_new_user)
    return {"Message": "User created"}


def login(request: Request, user: UserLogin, db: Session):
    user_db = db.query(User).filter(User.username == user.username).first()
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    if not verify_password(user.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return {
        "access_token": create_jwt_token(
            {"id": user_db.id, "username": user_db.username}
        ),
        "refresh_token": create_refresh_token(
            {"id": user_db.id, "username": user_db.username}
        ),
    }


@access_token_required
def all_user(request: Request, db: Session):
    all_user = db.query(User).all()
    return all_user


def get_user_by_id(id:int, request:Request, db:Session):
    user = db.query(User).get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    print(user.posts)
    for i in user.posts:
        print(i.location)
    return user