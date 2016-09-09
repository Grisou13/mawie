import datetime
from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.models import Movie

from app.models.base import Base


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    path = Column(Text)
    movie_id = Column(Integer, ForeignKey("movie.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
