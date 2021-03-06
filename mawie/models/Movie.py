from sqlalchemy import Boolean
from sqlalchemy import Column, Integer, String, Text, Date, Time, schema
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

from .db import db


# almost all the fields are completly empty since we can't be 100% sure imdb won't just fuck us over
class Movie(db.Model):
    __tablename__ = "movie"
    name = Column(String)
    imdb_id = Column(String)
    genre = Column(String, nullable=True)
    desc = Column(Text, nullable=True)
    release = Column(Date, nullable=True)
    runtime = Column(String, nullable=True)
    actors = Column(String, nullable=True)
    directors = Column(String, nullable=True)
    writer = Column(String, nullable=True)
    poster = Column(Text, nullable=True)  # can be an image in cache or a direct url to the website
    rate = Column(String, nullable=True)
    #raings = Column(Integer,nullable=True)
    files = relationship("File",primaryjoin="and_(File.movie_id == Movie.id, File.is_deleted==0)")
    viewed= Column(Boolean, default=False)
    def __str__(self):
        return self.name



if __name__ == '__main__':
    pass
