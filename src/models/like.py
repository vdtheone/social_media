from sqlalchemy import Column, ForeignKey, Integer

from src.config import Base

# class Like(Base):
#     __tablename__ = "likes"

#     id = Column(Integer, primary_key=True, index=True)
#     is_liked = Column(Boolean, default=False)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     post_id = Column(Integer, ForeignKey("posts.id"))

#     # users = relationship("User", back_populates="likes")
#     posts = relationship("Post", back_populates='likes')


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
