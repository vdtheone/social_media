from datetime import datetime

from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.models.post import Post
from src.models.user import User
from src.schemas.user import CreateUserSchema, UpdateUser, UserLogin
from src.utils.generate_jwt_token import (
    create_jwt_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)
from src.utils.required_jwt import access_token_required


def Oauth2Login(oauth2formdata: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter(User.username == oauth2formdata.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    if not verify_password(oauth2formdata.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    access_token = create_jwt_token({"id": user.id, "username": user.username})

    token = {"access_token": access_token, "token_type": "bearer"}
    return token


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


def get_user_by_id(id: int, db: Session):
    user = (
        db.query(User)
        .filter(User.id == id, User.is_active is True, User.is_deleted is False)
        .first()
    )
    # user = db.query(User).order_by(desc(User.liked_posts)).all()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def get_all_post_by_user(id: int, request: Request, db: Session):
    user = (
        db.query(User)
        .filter(User.id == id, User.is_active is True, User.is_deleted is False)
        .first()
    )
    post = (
        db.query(Post).filter(Post.user_id == id).order_by(desc(Post.created_at)).all()
    )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"user_name": user.username, "post": post}


def update_user_details(id: int, request: Request, user: UpdateUser, db: Session):
    user_instance = db.query(User).get(id)
    user_instance.first_name = user.first_name
    user_instance.last_name = user.last_name
    user_instance.mobile_no = user.mobile_no
    user_instance.username = user.username
    user_instance.password = user.password
    user_instance.updated_at = datetime.now()
    db.commit()
    db.refresh(user_instance)
    return user_instance


def delete_user(id: int, request: Request, db: Session):
    user = db.query(User).get(id)
    user.is_active = False
    user.is_deleted = True
    db.commit()
    db.refresh(user)
    return {"message": "User Deleted"}
