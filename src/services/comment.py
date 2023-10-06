from fastapi import Request
from src.models.comment import Comment
from src.schemas.comment import CommentSchema
from sqlalchemy.orm import Session
from src.utils.currunt_user_id import get_current_user_id


def add_new_comment(post_id:int, request:Request, comment:CommentSchema, db:Session):
    new_comment = Comment(
        desc = comment.desc,
        user_id = get_current_user_id(request),
        post_id = post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {"Message":"New comment added"}