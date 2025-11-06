from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .mixins import SoftDeleteMixin, TimestampMixin
from ..database import Base


class PostTable(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key = True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(50), index=True, nullable=False)
    content = Column(String(200), nullable=False)
    
    author = relationship("UserTable", lazy="joined", back_populates="posts")
    comments = relationship("CommentTable", lazy='selectin', back_populates="post")
    tags = relationship("PostTagTable", lazy="joined", back_populates="posts")