from typing import Union
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from src.config import SessionLocal
from src.utils.generate_jwt_token import create_jwt_token
from src.services.user import all_user, create_user_new, delete_user, get_all_post_by_user, get_user_by_id, login, update_user_details
from src.schemas.user import GetUser, UpdateUser, UserLogin, CreateUserSchema, UserWithPosts


user_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()


@user_router.post("/create")
async def create_user(request:Request, user:CreateUserSchema,  db: Session = Depends(get_db)):
    message = create_user_new(request, user, db)
    return message


@user_router.post('/login')
async def login_user(request:Request, user:UserLogin, db:Session = Depends(get_db)):
    message = login(request,user,db)
    return message


@user_router.get("/all", response_model=list[GetUser])
async def get_all_user(request:Request, db: Session = Depends(get_db)):
    return all_user(request, db)


@user_router.get("/user/{id}", response_model=UserWithPosts)
def user_by_id(id:int, request:Request, db:Session = Depends(get_db)):
    user = get_user_by_id(id, request, db)
    return user


@user_router.get("/posts/{id}")
def all_post_by_user(id:int, request:Request, db:Session = Depends(get_db)):
    post = get_all_post_by_user(id, request, db)
    return post


@user_router.put("/user/{id}", response_model=GetUser)
def update_user(id:int, request:Request, user:UpdateUser, db:Session = Depends(get_db)):
    return update_user_details(id, request, user, db)


@user_router.delete("/user/{id}")
def delete(id:int, request:Request, db:Session = Depends(get_db)):
    return delete_user(id, request, db)