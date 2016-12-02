import datetime
from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.models import Movie

from app.models import db
class File(db.Model):
    __tablename__ = "file"
    path = Column(Text)
    movie_id = Column(Integer, ForeignKey("movie.id"))
    movie = relationship("Movie", backref="movie")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
