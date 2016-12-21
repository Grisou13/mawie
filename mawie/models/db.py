import os
import re

from active_alchemy import ActiveAlchemy

from mawie import helpers

connection_string = helpers.DB_PATH
if connection_string.startswith('sqlite'):
    db_file = re.sub("sqlite.*:///", "", connection_string)
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    with open(db_file,"w+"): pass
db = ActiveAlchemy(connection_string)