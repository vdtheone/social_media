from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from src.services.post_services import create_post
from src.schemas.post_schema import PostSchema
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