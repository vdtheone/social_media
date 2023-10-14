from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.follower import Follower
from src.models.user import User
from src.schemas.follower import FollowRequestSchema


def follow_request(follow_request_schema: FollowRequestSchema, user, db: Session):
    if user.id == follow_request_schema.follow_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allow to follow your self",
        )

    already_following = (
        db.query(Follower)
        .filter(
            Follower.follow_by_id == user.id,
            Follower.follow_id == follow_request_schema.follow_id,
        )
        .first()
    )
    if already_following:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Already following"
        )

    db_user = db.query(User).get(follow_request_schema.follow_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    request_data = Follower(
        follow_by_id=user.id, follow_id=db_user.id, request="pending"
    )
    db.add(request_data)
    db.commit()
    db.refresh(request_data)
    return request_data


def unfollow_request(follow_request_schema: FollowRequestSchema, user, db: Session):
    following_user = (
        db.query(Follower)
        .filter(
            Follower.follow_by_id == user.id,
            Follower.follow_id == follow_request_schema.follow_id,
        )
        .first()
    )
    if not following_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.delete(following_user)
    db.commit()
    return {"message": "Unfollow user"}


def all_follower(user, db: Session):
    following_query = (
        db.query(User)
        .join(Follower, User.id == Follower.follow_by_id)
        .filter(Follower.follow_id == user.id, Follower.request == "accepted")
        .all()
    )
    return following_query


def all_following(user, db: Session):
    followers = db.query(Follower).filter(Follower.follow_by_id == user.id).all()
    follower_user_ids = [follower.follow_id for follower in followers]
    follower_users = db.query(User).filter(User.id.in_(follower_user_ids)).all()
    return follower_users


def feed(user, db: Session):
    following_query = (
        db.query(User)
        .join(Follower, User.id == Follower.follow_id)
        .filter(Follower.follow_by_id == user.id)
        .all()
    )
    all_posts = []
    for i in following_query:
        all_posts.append(i.posts)
    return all_posts


def all_request(user, db: Session):
    all_request = (
        db.query(Follower)
        .filter(Follower.follow_id == user.id, Follower.request == "pending")
        .all()
    )
    return all_request


def request_accept(id: int, user, db: Session):
    follower = db.query(Follower).get(id)
    user_foo = db.query(User).get(follower.follow_by_id)
    user_db = db.query(User).get(follower.follow_id)

    if follower.request == "accepted":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Already request accepted"
        )

    follower.request = "accepted"
    db.commit()
    db.refresh(follower)

    user_db.no_of_follower = user_db.no_of_follower + 1
    user_foo.no_of_following = user_foo.no_of_following + 1
    db.commit()
    db.refresh(user_db)
    db.refresh(user_foo)

    return {"message": "Request accepted"}


def request_delete(id: int, user, db: Session):
    follower = (
        db.query(Follower)
        .filter(Follower.id == id, Follower.request == "pending")
        .first()
    )
    if not follower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(follower)
    db.commit()
    return {"message": "Deleted"}
