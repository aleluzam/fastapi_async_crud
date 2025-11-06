from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .mixins import SoftDeleteMixin, TimestampMixin
from ..database import Base


class TagTable(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(50), index=True, nullable=False)
    use_counter = Column(String, default=0)
    



class PostTagTable(Base):
    __tablename__ = "post_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    
    posts = relationship("PostTable", lazy="selectin", back_populates="tags")
