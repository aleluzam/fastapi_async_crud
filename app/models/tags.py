from sqlalchemy import Column, String, Integer
from sqlalchemy.sql import func
from .mixins import SoftDeleteMixin, TimestampMixin
from ..database import Base


class TagTable(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(50), index=True, nullable=False)
    