from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.config import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    caption = Column(String)
    image = Column(String)
    number_of_likes = Column(Integer, default=0)
    number_of_comments = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    users = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="posts")

    # Relationship: Many-to-Many with User (to represent users who liked the post)
    likers = relationship("User", secondary="likes", back_populates="liked_posts")
