from sqlalchemy import Column, String, Integer
from sqlalchemy.sql import func
from .mixins import SoftDeleteMixin, TimestampMixin
from ..database import Base


class PostTable(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key = True, index=True)
    title = Column(String(50), index=True, nullable=False)
    content = Column(String(200), nullable=False)
    