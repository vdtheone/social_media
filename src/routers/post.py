from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Form, Request, UploadFile
from src.services.post import create_post, delete_all_post, delete_post, get_all_post, post_by_id, post_user, post_with_user_
from src.schemas.post import PostSchema, PostWithUser, PostWithUser_, SelectedPost
from src.config import SessionLocal


post_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@post_router.post("/create_post")
async def add_new_post(
    request: Request,
    location: Annotated[str, Form()],
    caption: Annotated[str, Form()],
    image: UploadFile,
    db: Session = Depends(get_db),
):
    message = await create_post(request, location, caption, image, db)
    return message


@post_router.get("/all_posts", response_model=List[PostSchema])
def get_all_post(request: Request, db: Session = Depends(get_db)):
    all_posts = get_all_post(request, db)
    return all_posts


@post_router.get("/post/{id}", response_model=PostSchema)
def get_one_post(id: int, request: Request, db: Session = Depends(get_db)):
    post = post_by_id(id, request, db)
    return post


@post_router.get("/post_user",response_model=List[PostWithUser_])
def get_post_with_user_(request: Request, db: Session = Depends(get_db)):
    return post_with_user_(request, db)
    

@post_router.get("/posts_user",response_model=List[PostWithUser])
def post_with_user(request: Request, db: Session = Depends(get_db)):
    return post_user(request, db)


@post_router.delete("/post/{id}")
def delete_one_post(id:int, request:Request, db:Session = Depends(get_db)):
    return delete_post(id, request, db) 


@post_router.delete("/post")
def delete_selected_post(request:Request, post:SelectedPost, db:Session = Depends(get_db)):
    return delete_all_post(request, post, db)