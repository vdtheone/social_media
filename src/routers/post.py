from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from src.services.post import create_post, get_all_post, post_by_id
from src.schemas.post import PostSchema
from src.config import SessionLocal



post_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()


@post_router.post("/create_post")
def add_new_post(request:Request, post:PostSchema, db:Session = Depends(get_db)):
    message = create_post(request, post, db)
    return message


@post_router.get("/all_posts", response_model=List[PostSchema])
def all_post(request:Request, db:Session = Depends(get_db)):
    all_posts = get_all_post(request, db)
    return all_posts


@post_router.get("/post/{id}", response_model=PostSchema)
def one_post(id:int, request:Request, db:Session = Depends(get_db)):
    post = post_by_id(id, request, db)
    return post