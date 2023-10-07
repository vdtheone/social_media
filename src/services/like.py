from fastapi import Request
from sqlalchemy.orm import Session
from src.models.post import Post
from src.models.like import Like
from src.utils.currunt_user_id import get_current_user_id


def like_post(id:int, request:Request, db:Session):
    userid = get_current_user_id(request)
    check_like = db.query(Like).filter(Like.user_id == userid).first()

    if check_like is not None and check_like.is_liked and check_like.post_id:
        check_like.is_liked = False
        db.commit()
        db.refresh(check_like)
        # decrese commnet count
        post = db.query(Post).get(id)
        post.number_of_likes-=1
        db.commit()
        db.refresh(post)
        return {"message":"Post Disliked"}
    
    elif check_like is not None and check_like.is_liked is False and check_like.post_id:
        check_like.is_liked = True
        db.commit()
        db.refresh(check_like)
        # increase comment count
        post = db.query(Post).get(id)
        post.number_of_likes+=1
        db.commit()
        db.refresh(post)
        return {"message":"Post Liked"}
    
    else:
        like = Like(
            is_liked = True,
            user_id = userid,
            post_id = id
        )
        db.add(like)
        db.commit()
        db.refresh(like)
        # increse comment count
        post = db.query(Post).get(id)
        post.number_of_likes+=1
        db.commit()
        db.refresh(post)
        return {"message":"Post Liked"}


def delete_all(db:Session):
    delete = db.query(Like).delete()
    db.commit()
    return {"message":"Delete all likes in table"}
