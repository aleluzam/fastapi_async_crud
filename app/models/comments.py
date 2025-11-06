from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .mixins import SoftDeleteMixin, TimestampMixin
from ..database import Base


class CommentTable(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key = True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    content = Column(String(200), nullable=False)
    
    author = relationship("UserTable", lazy="joined", back_populates="comments")
    post = relationship("PostTable", lazy="joined", back_populates="comments")