import os
# os.mkdir("./.cache")
# import pip
# pip.main(["install","-r","requirements.txt"])
# import sqlite3
# conn=sqlite3.connect('.cache/main.sqlite')
# import populate_db
# populate_db.populate()
from subprocess import call
for d,dn,fn in os.walk("conf/"):
    for f in fn:
        if f.endswith(".qrc"):
            call("pyrcc5.exe -o app/gui/resources/{}.py conf\{}".format(os.path.splitext(os.path.basename(f))[0],f))
