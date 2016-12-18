import asyncio
import os

import time
from PyQt5.QtCore import QThread

from mawie.events import Eventable, Listener
from mawie.events.app import Tick
from mawie.events.updator import UpdatorRequest
from mawie.models.File import File
from mawie.models.Movie import Movie
import logging
log = logging.getLogger(__name__)
class QUpdator(QThread):
    """Helper class to execute the updator in a QtAppliction
    This just proxies the updator into a thread, so it doesn't impact performance for the main Gui application.

    :Example:
    >>> qu = QUpdator()
    >>> qu.start()
    """
    def __init__(self,*arg,**kwargs):
        super(QUpdator,self).__init__(*arg,**kwargs)
    def start(self, priority=None):
        super(QUpdator,self).start()
    def run(self):
        updator = Updator()
        updator.run()

class Updator(Listener):
    def __init__(self):
        super(Updator, self).__init__()
        log.info("starting updator")
        self.previousRun = 0
        self._run = True
        self._running = False
        self._timeout = 6000
        #self.search = research.Research(model=File.File,cols=["path"])

        self.loop = asyncio.get_event_loop()
        #q = asyncio.Queue(loop=loop)
    async def procesFile(self):
        """
        Loops all files and delete it if it has no associated movie
        :return:
        """
        files = File.query(include_deleted=True)  # just search all files
        for f in files:
            if not os.path.exists(f.path):
                log.debug("file "+f.path+" does not exist")
                mov = f.movie
                if mov is None:
                    f.delete()
                    log.debug("deleting file "+f.path + ", it had no movies")
                elif len(mov.files) == 1: #if the movie has only 1 file, then we can confidently remove it from the db
                    mov.files.remove(f)
                    f.delete()
                    mov.delete()
                    log.debug("deleting file" + f.path + ", it was associated with "+mov.name)
            await asyncio.sleep(self.timeout)
    async def processMovies(self):
        """
        Processes all movies that don't have any files, or files are deleted
        :return:
        """
        movies = Movie.query(include_deleted=True)
        for m in movies:
            if not m.is_deleted and len(m.files) < 1:
                m.delete()
                log.debug("deleting movie "+m.name+ ", it had no file")
            elif m.is_deleted: #if th emovie is deleted, we check it doesnt have any files. If it does, delete the files
                if len(m.files) >= 1:
                    files = m.files
                    for f in files:
                        f.delete()
                    m.files.delete()
            await asyncio.sleep(self.timeout)#just wait
    def run(self):
        """
        Runs both process methods in an aysncio loop
        :return:
        """
        log.info("starting updator run [timeout = %s] [previous run = %s]",self._timeout,self.previousRun)
        self._running = True
        loop = self.loop
        loop.run_until_complete(self.procesFile())
        loop.run_until_complete(self.processMovies())
        loop.close()
        self.previousRun = time.time()
        self._running = False
    def handle(self,event):
        if isinstance(event, UpdatorRequest):
            if event.data == -1:
                log.info("stopping updator")
                self._run = False
            self._timeout = event.data
            log.info("updated updator time to = %s", event.data)
        if isinstance(event,Tick):
            if self._run and not self._running and self.previousRun + self._timeout >= event.data:
                self.run()

if __name__ == '__main__':
    u = Updator()
    u.run()