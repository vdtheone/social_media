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
        .filter(Follower.follow_id == follow_request_schema.follow_id)
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

    request_data = Follower(follow_by_id=user.id, follow_id=db_user.id)
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
        .filter(Follower.follow_id == user.id)
        .all()
    )
    print("following_query = ", following_query)
    all_followers = []
    for i in following_query:
        all_followers.append(i)
    return all_followers


def all_following(user, db: Session):
    followers = db.query(Follower).filter(Follower.follow_by_id == user.id).all()
    follower_user_ids = [follower.follow_id for follower in followers]
    follower_users = db.query(User).filter(User.id.in_(follower_user_ids)).all()
    all_followings = []
    for i in follower_users:
        all_followings.append(i.__dict__)
        print(i.first_name)
    return all_followings


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
