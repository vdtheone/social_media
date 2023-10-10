from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.config import SessionLocal
from src.services.like import delete_all, like_post

like_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@like_router.post("/add_like/{id}")
def add_like(id: int, request: Request, db: Session = Depends(get_db)):
    return like_post(id, request, db)


@like_router.delete("/delete_all")
def deleteall(db: Session = Depends(get_db)):
    return delete_all(db)
