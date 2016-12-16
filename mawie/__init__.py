import sys
import os
if __name__ == '__main__':#TODO this is a complete hack, this should be fioxed or use relative imports
    sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
    sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from mawie.helpers import LOG_PATH
import logging
import logging.handlers
s = '%(asctime)4s %(name)-16s %(levelname)-8s [%(threadName)-10s] [PID = %(process)-5s]  %(message)s'
formatter = logging.Formatter(s)
#basic config
logging.basicConfig(level=logging.INFO, format=s, filemode = "w+")
logger = logging.getLogger("mawie")
#define handlers
default = logging.handlers.RotatingFileHandler(os.path.join(LOG_PATH,'app.log'),"a+",encoding="utf8",backupCount = 5)
default.setLevel(logging.INFO)
default.setFormatter(formatter)
error = logging.FileHandler(os.path.join(LOG_PATH,'error.log'))
error.setLevel(logging.WARNING)
error.setFormatter(formatter)
debug = logging.FileHandler(os.path.join(LOG_PATH,'debug.log'))
debugForm = logging.Formatter("[%(asctime)s %(relativeCreated)6d] [%(threadName)s %(process)d]  [%(levelname)-8s] [%(pathname)s %(module)s %(funcName)s] %(message)s")
debug.setLevel(logging.DEBUG)
debug.setFormatter(debugForm)
#assign them
logger.addHandler(debug)
logger.addHandler(error)
logger.addHandler(default)

def app():
    from mawie.app import start
    return start()

if __name__ == '__main__':
    app()