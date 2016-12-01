import asyncio
import os
import threading

from app.eventable import Eventable
from app.models import File
from app.models.Movie import Movie
from app.research import research
class Worker(threading.Thread):
    def run(self):
        pass
#TODO profile this, and verify memory usage
class Updator(Eventable):
    def __init__(self):
        self.timeout = 60  # every minute
        if __name__ == '__main__':
            self.timeout = 1

        self.search = research.Research(model=File.File,cols=["path"])

        self.loop = asyncio.get_event_loop()
        #q = asyncio.Queue(loop=loop)
    async def procesFile(self):
        files = self.search.search()  # just search all files
        for f in files:
            if not os.path.exists(f.path):
                mov = f.movie
                if len(mov.files) == 2: #if the movie has only 1 file, then we can confidently remove it from the db
                    mov.files.remove(f)
            await asyncio.sleep(self.timeout)
    async def processMovies(self):
        search = self.search
        search.setModel(Movie)
        search.setCols(["name"])
        movies = search.search()
        for m in movies:
            if len(m.files < 1):
                m.delete()
            await asyncio.sleep(self.timeout)#just wait
    def run(self):
        loop = self.loop
        loop.run_until_complete(self.procesFile())
        loop.close()
if __name__ == '__main__':
    u = Updator()
    u.run()