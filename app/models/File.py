import datetime
from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from .Movie import Movie

Base = declarative_base()


class File(Base):
    id = Column(Integer, primary_key=True)
    path = Column(Text)
    id_movie = Column(ForeignKey("movie.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    movie = relationship(Movie)
