from fastapi import HTTPException, Request, status
from src.schemas.post import PostSchema
from src.models.post import Post
from sqlalchemy.orm import Session
from jose import jwt
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def create_post(request:Request, post:PostSchema, db:Session):
    access_token = request.headers.get("Authorization").split()[1]
    user_id = (jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])).get('id')
    new_post = Post(
        location = post.location,
        caption = post.caption,
        upload_time = post.upload_time,
        number_of_likes = post.number_of_likes,
        number_of_comments = post.number_of_comments,
        user_id = user_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"Message":"Post Created"}


def get_all_post(request:Request, db:Session):
    all_post = db.query(Post).all()
    return all_post


def post_by_id(id:int, request:Request, db:Session):
    post = db.query(Post).get(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # print(post.users.username) #get user by post
    return post