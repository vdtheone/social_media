from fastapi import APIRouter, Depends, Request
from src.services.comment import add_new_comment
from src.schemas.comment import CommentSchema
from src.config import SessionLocal
from sqlalchemy.orm import Session

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

comment_router = APIRouter()


@comment_router.post("/new_comment/{post_id}")
def add_comment(post_id:int, request:Request, comment:CommentSchema, db:Session = Depends(get_db)):
    responce = add_new_comment(post_id, request, comment, db)
    return responce