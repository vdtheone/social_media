from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config import SessionLocal
from src.models.user import User
from src.schemas.follower import FollowRequestSchema, UserSchemaFollower
from src.schemas.user import GetUser
from src.services.follower import (
    all_follower,
    all_following,
    all_request,
    feed,
    follow_request,
    request_accept,
    request_delete,
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
    user.followers
    return all_follower(user, db)


@follower_router.get("/following", response_model=List[UserSchemaFollower])
def get_all_following(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return all_following(user, db)


@follower_router.get("/feed")
def user_feed(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return feed(user, db)


@follower_router.get("/request")
def get_follow_requests(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return all_request(user, db)


@follower_router.get("/accept_request/{id}")
def accept_request(
    id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return request_accept(id, user, db)


@follower_router.delete("/delete_request/{id}")
def delete_request(
    id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return request_delete(id, user, db)
