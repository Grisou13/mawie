import sys
import os

from mawie.helpers import LOG_PATH

if __name__ == '__main__':#TODO this is a complete hack, this should be fioxed or use relative imports
    sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
    sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import logging
import logging.handlers
s = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
formatter = logging.Formatter(s)
#basic config
logging.basicConfig(level=logging.NOTSET, format=s, filemode = "w+")
logger = logging.getLogger("mawie")
#define handlers
default = logging.handlers.RotatingFileHandler(os.path.join(LOG_PATH,'app.log'),"a+",encoding="utf8",backupCount = 5)
default.setLevel(logging.INFO)
default.setFormatter(formatter)
error = logging.FileHandler(os.path.join(LOG_PATH,'error.log'))
error.setLevel(logging.WARNING)
error.setFormatter(formatter)
debug = logging.FileHandler(os.path.join(LOG_PATH,'debug.log'))
debugForm = logging.Formatter("[%(asctime)s %(relativeCreated)s ] [%(threadName)s %(process)d]  [%(levelname)-8s] [%(pathname)s %(module)s %(funcName)s] %(message)s")
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