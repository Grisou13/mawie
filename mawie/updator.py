import asyncio
import logging
import os
import time

from mawie.events import Listener, Start
from mawie.events.app import Tick
from mawie.events.updator import UpdatorRequest, ForceUpdatorRun
from mawie.models.File import File
from mawie.models.Movie import Movie
from queue import Queue

log = logging.getLogger(__name__)


class Updator(Listener):
    """
    The updator does exactly what it's name indicates. It updates the list of movies with the list of files that were stored by the app. It checks whether they exist, and then updates the databasse accordingly
    Asyncio was used just to test it out on small component. It wasn't that great of an idea...
    """

    def __init__(self):
        super(Updator, self).__init__()
        log.info("starting updator")
        self.previousRun = 0
        self._run = True
        self._running = False
        self._timeout = 6000
        self._sleep = 10
        self._files = Queue(-1)
        self._movies = Queue(-1)

    async def procesFiles(self):
        """
        Loops all files and delete it if it has no associated movie
        :return:
        """
        while not self._files.qsize() == 0:
            f = self._files.get(True, 0.1)
            self.processFile(f)
            await asyncio.sleep(self._sleep)

    async def processMovies(self):
        """
        Processes all movies that don't have any files, or files are deleted
        :return:
        """
        while not self._movies.qsize() == 0:
            m = self._movies.get(True, 0.1)
            self.processMovie(m)
            await asyncio.sleep(self._sleep)  # just wait

    def processFile(self, file_):
        """
        processes a single file. This will check if the file exists on disk.
        :param file_: File model
        :type file_: File
        :return:
        """
        if not os.path.exists(file_.path):
            log.debug("file " + file_.path + " does not exist")
            mov = file_.movie
            if mov is None:
                file_.delete()
                log.debug("deleting file " + file_.path + ", it had no movies")
            elif len(mov.files) == 1:  # if the movie has only 1 file, then we can confidently remove it from the db
                mov.files.remove(file_)
                file_.delete()
                mov.delete()
                log.debug("deleting file" + file_.path + ", it was associated with " + mov.name)

    def processMovie(self, mov):
        """
        Processes a single movie. This will delete a movie if it doesn't have any files
        :param mov: Movie model
        :type mov: Movie
        :return:
        """
        if not mov.is_deleted and len(mov.files) < 1:
            mov.delete()
            log.debug("deleting movie " + mov.name + ", it had no file")
        elif mov.is_deleted:  # if th emovie is deleted, we check it doesnt have any files. If it does, delete the files
            if len(mov.files) >= 1:
                files = mov.files
                for f in files:
                    f.delete()
                mov.files.delete()

    def run(self):
        """
        Runs both process methods in an aysnc loop
        :return:
        """
        log.info("starting updator run [current time = %s] [timeout = %s] [previous run = %s]", time.time(),
                 self._timeout, self.previousRun)
        if not hasattr(self,"emit"):
            self.runBlocking()
            return
        self._running = True
        # populate the queues
        for m in Movie.query(include_deleted=True):
            self._movies.put(m, True, 0.1)
        for f in File.query(include_deleted=True):
            self._files.put(f, True, 0.1)
        log.info("updator queues will start processing [movies = %s] [files = %s]", self._movies.qsize(),
                 self._files.qsize())
        self.process()  # start the processing

    def runBlocking(self):
        """
        This will do the same as run, but in a blocking way.
        It will process everything before returning handle of the thread.
        If you want to use this, you should use it in a separate thread.
        This method will be used in run() if the updator doesn't have any emit function
        :return:
        """
        log.info("starting updator run [current time = %s] [timeout = %s] [previous run = %s]", time.time(),
                 self._timeout, self.previousRun)
        self._running = True
        for m in Movie.query(include_deleted=True):
            self._movies.put(m, True, 0.1)
        for f in File.query(include_deleted=True):  # just search all files
            self._files.put(f, True, 0.1)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.procesFiles())
        loop.run_until_complete(self.processMovies())
        loop.close()
        self.previousRun = time.time()
        self._running = False

    def process(self):
        """
        This function is called on every tick of the updator. It is used to process files one by one
        :return:
        """
        log.info("processing files and movies for updator [time = %s]", time.time())
        if self._files.qsize() == 0 and self._movies.qsize() == 0:
            self._running = False
            self.previousRun = time.time()
            return
        if not self._files.qsize() == 0:
            f = self._files.get(True, 0.1)
            self.processFile(f)
            self._files.task_done()
        if not self._movies.qsize() == 0:
            m = self._movies.get(True, 0.1)
            self.processMovie(m)
            self._movies.task_done()

    def handle(self, event):
        if isinstance(event, UpdatorRequest):
            if event.data == -1:
                log.info("stopping updator")
                self._run = False
            self._timeout = event.data
            log.info("updated updator time to = %s", event.data)
        elif isinstance(event, Start):
            self._run = True
            self._running = False
        elif isinstance(event, ForceUpdatorRun):
            #empty the queues before running
            while self._movies.qsize() > 0:
                m = self._movies.get(True,0.1)
                self._movies.task_done()
            while self._files.qsize() > 0:
                m = self._files.get(True,0.1)
                self._files.task_done()
            self.run()
        elif isinstance(event, Tick):
            if self._run:
                if not self._running:
                    if self.previousRun + self._timeout <= event.data:  # we can run the updator, it has waited the apropriate time before rerunning
                        self.run()
                else:
                    self.process()


if __name__ == '__main__':
    u = Updator()
    u.run()
