from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.config import Base

# from models.like import Like
# from models.post import Post

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    mobile_no = Column(Integer)
    username = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)   
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


    posts = relationship("Post", back_populates='users')
    # # comments = relationship("Comment", back_populates='users')
    # likes = relationship("Like", back_populates='users')
