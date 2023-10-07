from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.config import Base

# from src.models.user import User
# from src.models.like import Like

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    caption = Column(String)
    upload_time = Column(DateTime, default=datetime.now())
    number_of_likes = Column(Integer, default=0)
    number_of_comments = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates='posts')
    likes = relationship("Like", back_populates='posts')