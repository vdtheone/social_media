from pathlib import Path
from typing import Annotated
from fastapi import Form, HTTPException, Request, UploadFile, status
from src.models.post import Post
from src.utils.currunt_user_id import get_current_user_id
from sqlalchemy.orm import Session
import os

IMGDIR = "images"

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


async def create_post(
    request: Request,
    location: Annotated[str, Form()],
    caption: Annotated[str, Form()],
    image: UploadFile,
    db: Session,
):
    user_id = get_current_user_id(request)
    data = await image.read()
    content_type = image.content_type
    filename = image.filename

    if not content_type == "image/jpeg":
        raise HTTPException(status_code=403, detail="Invalid format")

    # Create the folder if it doesn't exist
    Path(IMGDIR).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(IMGDIR, filename), "wb") as my_file:
        my_file.write(data)

    new_post = Post(location=location, caption=caption, image=filename, user_id=user_id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"Message": "Post Created"}


def get_all_post(request: Request, db: Session):
    all_post = db.query(Post).all()
    return all_post


def post_by_id(id: int, request: Request, db: Session):
    post = db.query(Post).get(id)

    with open(os.path.join(IMGDIR, post.image), "rb") as my_file:
        data = my_file.read()
    
    print(data)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


def post_with_user_(request: Request, db: Session):
    posts = db.query(Post).all()

    for post in list(posts):
        post.__dict__.update({"username": post.users.username})

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return posts


def post_user(request: Request, db: Session):
    posts = db.query(Post).all()
    post_list = []
    for post in posts:
        post_dict = {}
        post_dict["username"] = post.users.username
        post_dict["post"] = post
        post_list.append(post_dict)

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post_list
