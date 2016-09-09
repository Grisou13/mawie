from datetime import datetime

import timestring as timestring
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models.base as base
import app.models.File as f
import app.models.Movie as m
import app.helpers as H
try:
    engine = create_engine(H.DB_PATH)
    base.Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    m1 = m.Movie()
    m1.name     = "The Hangover Part II"
    m1.desc     = "Right after the bachelor party in Las Vegas, Phil, Stu, Alan, and Doug jet to Thailand for Stu's wedding. Stu's plan for a subdued pre-wedding brunch, however, goes seriously awry."
    m1.actors   = "Bradley Cooper, Zach Galifianakis, Ed Helms, Justin Bartha"
    m1.imdb_id  = "tt1411697"
    m1.poster   = "http://ia.media-imdb.com/images/M/MV5BMTM2MTM4MzY2OV5BMl5BanBnXkFtZTcwNjQ3NzI4NA@@._V1_SX320.jpg"
    m1.runtime  = "1 hr 42 mins"
    m1.release  = datetime.fromtimestamp(timestring.Date("26 May 2011").to_unixtime())
    m1.genre    = "Comedy"
    f1 = f.File()
    f1.path="stubs/FILM_A_TRIER/BATMAN.avi"
    m1.files.append(f1)
    session.add(m1)
    session.commit()
except ValueError as e:
    print(e)
