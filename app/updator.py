import asyncio
import os

from PyQt5.QtCore import QThread

from app.events import Eventable
from app.models.File import File
from app.models.Movie import Movie
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
#TODO profile this, and verify memory usage
class Updator(Eventable):
    def __init__(self):
        super(Updator, self).__init__()
        self.timeout = 60  # every minute
        if __name__ == '__main__':
            self.timeout = 1

        #self.search = research.Research(model=File.File,cols=["path"])

        self.loop = asyncio.get_event_loop()
        #q = asyncio.Queue(loop=loop)
    async def procesFile(self):
        files = File.query(include_deleted=True)  # just search all files
        for f in files:
            if not os.path.exists(f.path):
                print("file "+f.path+" does not exist")
                mov = f.movie
                if mov is None:
                    f.delete()
                    print("deleting file "+f.path + ", it had no movies")
                elif len(mov.files) == 1: #if the movie has only 1 file, then we can confidently remove it from the db
                    mov.files.remove(f)
                    f.delete()
                    mov.delete()
                    print("deleting file" + f.path + ", it was associated with "+mov.name)
            await asyncio.sleep(self.timeout)
    async def processMovies(self):
        movies = Movie.query(include_deleted=True)
        for m in movies:
            if not m.is_deleted and len(m.files) < 1:
                m.delete()
                print("deleting movie "+m.name+ ", it had no file")
            elif m.is_deleted: #if th emovie is deleted, we check it doesnt have any files. If it does, delete the files
                if len(m.files) >= 1:
                    files = m.files
                    for f in files:
                        f.delete()
                    m.files.delete()
            await asyncio.sleep(self.timeout)#just wait
    def run(self):
        loop = self.loop
        loop.run_until_complete(self.procesFile())
        loop.run_until_complete(self.processMovies())
        loop.close()
        print("finished")
if __name__ == '__main__':
    u = Updator()
    u.run()