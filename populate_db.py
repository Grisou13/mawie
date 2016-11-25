import os
import urllib.request
from datetime import datetime
import timestring as timestring
import app.models.Movie as m
import app.models.File as f
from app.models import db
import omdb
def get_films():
    _raw = omdb.request(s="The H", plot="short", r="json").json()
    if "Search" in _raw:
        films = _raw["Search"]
        for f in films:
            film = omdb.imdbid(f["imdbID"])
            yield dict( (k.lower(), (None if v == 'N/A' else v)) for k,v in film.items() )

db.drop_all() # clear the database you know?
db.create_all() # and redo it aha
for l in get_films():
    m1 = m.Movie()
    m1.name     = l["title"]
    m1.desc     = l["plot"]
    m1.actors   = l["actors"]
    m1.imdb_id  = l["imdb_id"]
    m1.poster   = l["poster"]
    m1.runtime  = l["runtime"]
    m1.release  = (datetime.strptime(l["released"],"%d %b %Y") if l["released"] is not None else None)
    m1.genre    = l["genre"]
    f1 = f.File()
<<<<<<< HEAD
    f1.path="stubs/"+l["title"]+".avi"
=======
    f1.path=os.path.realpath("stubs/"+l["title"]+".avi")
>>>>>>> develop

    m1.files.append(f1)
    f1.save()
    m1.save()

print("finihsed")
