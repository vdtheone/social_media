from fastapi import HTTPException, Request, status
from src.models.comment import Comment
from src.models.post import Post
from src.models.user import User
from src.schemas.comment import CommentSchema
from sqlalchemy.orm import Session
from src.utils.currunt_user_id import get_current_user_id


def add_new_comment(
    post_id: int, request: Request, comment: CommentSchema, db: Session
):
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    userid = get_current_user_id(request)
    user = db.query(User).get(userid)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    new_comment = Comment(desc=comment.desc, user_id=userid, post_id=post.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"Message": "New comment added"}


def delete_user_comment(id: int, request: Request, db: Session):
    comment = db.query(Comment).get(id)
    db.delete(comment)
    db.commit()
    return {"message":"commnet deleted"}