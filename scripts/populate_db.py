import os
if __name__ == '__main__':
    import sys
    sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__),"../")))
import urllib.request
from datetime import datetime
import app.helpers as h
import re
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
def populate():
    try:
        os.mkdir(os.path.join(os.path.dirname(__file__),"../stubs"))
    except:
        pass
    db.drop_all()  # clear the database you know?
    db.create_all()  # and redo it aha
    for l in get_films():
        title = re.sub('[^\w_.)( \-\s]', '', l["title"])
        m1 = m.Movie()
        m1.name = l["title"]
        m1.desc = l["plot"]
        m1.actors = l["actors"]
        m1.imdb_id = l["imdb_id"]
        m1.poster = l["poster"]
        m1.runtime = l["runtime"]
        m1.release = (datetime.strptime(l["released"], "%d %b %Y") if l["released"] is not None else None)
        m1.genre = l["genre"]
        f1 = f.File()
        f1.path = os.path.realpath(os.path.join(h.BASE_PATH,"stubs/" ,title.replace(" ","_") + ".avi"))
        m1.files.append(f1)
        f1.save()
        m1.save()
        with open(f1.path,"w+") as s:pass

if __name__ == '__main__':

    try:
        os.mkdir(h.CACHE_PATH)
    except:
        pass
    if not os.path.exists(h.DB_PATH):
        with open(h.DB_PATH,"w+"):pass
    populate()
    print("finished")
