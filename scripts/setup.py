import app.helpers as h

import os
# os.mkdir(h.CACHE_PATH)
# import pip
# pip.main(["install","-r",h.BASE_PATH+"/requirements.txt"])
# import sqlite3
# conn=sqlite3.connect(h.DB_FILE)
# import populate_db
# populate_db.populate()
from subprocess import call
for d,dn,fn in os.walk(h.BASE_PATH+"/resources/"):
    for f in fn:
        if f.endswith(".qrc"):
            call("pyrcc5.exe  -o "+h.BASE_PATH+"/app/gui/resources/{}.py "+h.BASE_PATH+"/resources/{}".format(os.path.splitext(os.path.basename(f))[0],f))
