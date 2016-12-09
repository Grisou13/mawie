import mawie.helpers as h
from subprocess import call
import os
from .populate_db import populate
def createResources():
    for d,dn,fn in os.walk(h.BASE_PATH+"/resources/"):
        for f in fn:
            if f.endswith(".qrc"):
                call("pyrcc5.exe  -o "+h.BASE_PATH+"/mawie/gui/resources/{}.py "+h.BASE_PATH+"/resources/{}".format(os.path.splitext(os.path.basename(f))[0],f))
def createPaths():
    os.mkdir(h.CACHE_PATH)
    import sqlite3
    conn = sqlite3.connect(h.DB_FILE) # creates the db file
    conn.close()
def seedDb():
    populate()
def installPip():
    call("cd "+h.BASE_PATH+" && pip install -r requirements.txt")
def run(pip=True):
    if pip:
        installPip()
    createPaths()
    createResources()
    seedDb()
if __name__ == '__main__':
    run()