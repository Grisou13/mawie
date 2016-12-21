import datetime
import os

from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .db import db

class File(db.Model):
    __tablename__ = "file"
    path = Column(Text)
    base = Column(Text, nullable=True)
    movie_id = Column(Integer, ForeignKey("movie.id"))
    movie = relationship("Movie", backref="movie")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    @hybrid_property
    def directory(self):
        return os.path.basename(self.path)
