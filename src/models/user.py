from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.config import Base
from src.models.follower import Follower

# from models.like import Like
# from models.post import Post


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    mobile_no = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    no_of_follower = Column(Integer, default=0)
    no_of_following = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    posts = relationship("Post", back_populates="users")
    comments = relationship("Comment", back_populates="users")

    # Relationship: Many-to-Many with Post (to represent liked posts)
    liked_posts = relationship("Post", secondary="likes", back_populates="likers")

    followers = relationship(
        "Follower", foreign_keys=[Follower.follow_id], backref="followed_user"
    )
