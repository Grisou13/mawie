import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(Text)
    release = Column(Date)
    runtime = Column(Time)
    actors = Column(String)
    directors = Column(String, nullable = True)
    writer = Column(String , nullable=True)
    poster = Column(Text,nullable=True) #can be an image in cache or a direct url to the website


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)