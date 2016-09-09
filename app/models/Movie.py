import os
import sys

import datetime
from sqlalchemy import Column,  Integer, String, Text, Date, Time, schema
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import app.helpers
from app.models.base import Base

#almost all the fields are completly empty since we can't be 100% sure imdb won't just fuck us over
class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    imdb_id=Column(String)
    genre = Column(String, nullable=True)
    desc = Column(Text, nullable=True)
    release = Column(Date, nullable=True)
    runtime = Column(String, nullable=True)
    actors = Column(String, nullable=True)
    directors = Column(String, nullable = True)
    writer = Column(String , nullable=True)
    poster = Column(Text,nullable=True) #can be an image in cache or a direct url to the website
    #raings = Column(Integer,nullable=True)
    files = relationship("File", backref="Movie.id")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

if __name__ == '__main__':
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine(app.helpers.DB_PATH)

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)