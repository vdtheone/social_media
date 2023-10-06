from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from src.config import SessionLocal
from src.utils.generate_jwt_token import create_jwt_token
from src.services.user import all_user, create_user_new, get_user_by_id, login
from src.schemas.user import GetAllUser, UserLogin, CreateUserSchema


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


@user_router.get("/all", response_model=list[GetAllUser])
async def get_all_user(request:Request, db: Session = Depends(get_db)):
    return all_user(request, db)


@user_router.get("/user/{id}", response_model=GetAllUser)
def user_by_id(id:int, request:Request, db:Session = Depends(get_db)):
    user = get_user_by_id(id, request, db)
    return user