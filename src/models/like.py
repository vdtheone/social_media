from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.config import Base



class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    is_liked = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    # users = relationship("User", back_populates="likes")
    # posts = relationship("Post", back_populates='likes')