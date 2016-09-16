import os
import urllib.request
from datetime import datetime
import timestring as timestring
import app.models.Movie as m
import app.models.File as f
from app.models import db
import app.helpers as H
import json
def get_films():
    with open(os.path.join(H.CACHE_PATH, "films.json"),"w+") as f:
        _raw = urllib.request.urlopen("http://www.omdbapi.com/?s=The+H&y=&plot=short&r=json").read()
        f.write(_raw.decode("utf-8"))
        j = json.loads(_raw.decode("utf-8"))
        if "Search" in j.keys():
            films = j["Search"]
            for f in films:
                _raw = urllib.request.urlopen("http://www.omdbapi.com/?i="+f["imdbID"]).read()
                film = json.loads(_raw.decode("utf-8"),"utf-8")
                yield dict( (k.lower(), (None if v == 'N/A' else v)) for k,v in film.items() )

db.drop_all() # clear the database you know?
db.create_all() # and redo it aha
for l in get_films():
    m1 = m.Movie()
    m1.name     = l["title"]
    m1.desc     = l["plot"]
    m1.actors   = l["actors"]
    m1.imdb_id  = l["imdbid"]
    m1.poster   = l["poster"]
    m1.runtime  = l["runtime"]
    m1.release  = (datetime.strptime(l["released"],"%d %b %Y") if l["released"] is not None else None)
    m1.genre    = l["genre"]
    f1 = f.File()
    f1.path="stubs/"+l["title"]+".avi"
    m1.files.append(f1)
    f1.save()
    m1.save()
print("finihsed")
