import datetime
import os

from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.models import Movie

from app.models.base import Base
# TODO: redo models with https://github.com/mardix/active-alchemy
from app.models import db
class File(db.Model):
    __tablename__ = "file"
    path = Column(Text)
    movie_id = Column(Integer, ForeignKey("movie.id"))
    movie = relationship("Movie", backref="movie")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    base = Column(Text, nullable=True)


def directory(self):
        return os.path.basename(self.path)
