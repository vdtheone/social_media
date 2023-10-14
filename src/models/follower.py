from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.config import Base, SessionLocal

db = SessionLocal()


class Follower(Base):
    __tablename__ = "followers"

    id = Column(Integer, primary_key=True, index=True)
    follow_by_id = Column(Integer, ForeignKey("users.id"))
    follow_id = Column(Integer, ForeignKey("users.id"))
    request = Column(String)

    following = relationship(
        "User", foreign_keys=[follow_by_id], backref="following_user"
    )
