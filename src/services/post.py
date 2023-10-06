from fastapi import HTTPException, Request, status
from schemas.post import PostSchema
from src.models.post import Post
from sqlalchemy.orm import Session
from jose import ExpiredSignatureError, JWTError, jwt
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
        number_of_like = post.number_of_likes,
        number_of_comments = post.number_of_comments,
        user_id = user_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"Message":"Post Created"}