from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config import SessionLocal
from src.models.user import User
from src.schemas.follower import FollowRequestSchema
from src.schemas.user import GetUser
from src.services.follower import (
    all_follower,
    all_following,
    feed,
    follow_request,
    unfollow_request,
)
from src.utils.current_user_dependency import get_current_user

follower_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@follower_router.post("/follow")
def follow_a_user(
    follow_request_schema: FollowRequestSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return follow_request(follow_request_schema, user, db)


@follower_router.post("/unfollow")
def unfollow_a_user(
    follow_request_schema: FollowRequestSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return unfollow_request(follow_request_schema, user, db)


@follower_router.get("/follower", response_model=List[GetUser])
def get_all_follower(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return all_follower(user, db)


@follower_router.get("/following", response_model=List[GetUser])
def get_all_following(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return all_following(user, db)


@follower_router.get("/feed")
def user_feed(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return feed(user, db)
