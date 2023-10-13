from sqlalchemy import Column, ForeignKey, Integer

from src.config import Base


class Follower(Base):
    __tablename__ = "followers"

    id = Column(Integer, primary_key=True, index=True)
    follow_by_id = Column(Integer, ForeignKey("users.id"))
    follow_id = Column(Integer, ForeignKey("users.id"))
