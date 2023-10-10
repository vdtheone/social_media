from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.event import listens_for
from sqlalchemy.orm import relationship

from src.config import Base, SessionLocal
from src.models.post import Post

db = SessionLocal()


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    users = relationship("User", back_populates="comments")
    posts = relationship("Post", back_populates="comments")


# This function will be called after a new comment is inserted
# increase comment count when new comment is add
@listens_for(Comment, "after_insert")
def increment_comment_count(mapper, connection, comment):
    post_id = comment.post_id
    post = db.query(Post).filter(Post.id == post_id).first()
    post.number_of_comments = post.number_of_comments + 1
    db.commit()
    db.refresh(post)
    # connection.execute(
    #     Post.__table__.update()
    #     .values(number_of_comments=post.number_of_comments)
    #     .where(Post.id == post_id)
    # )
