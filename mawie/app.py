import threading
import time
from queue import Queue, Empty

from mawie.events import Eventable, Start, EventManager, Response
from mawie.helpers import Singleton



from mawie.events.app import *

from mawie.explorer.explorer import Explorer
from mawie.research.research import Research
from mawie.explorer.googleit import googleIt
import logging
log = logging.getLogger("mawie")

class AppComponent(Eventable):
    pass


class App(EventManager):
    # based out of tornado ioloop https://github.com/tornadoweb/tornado/blob/master/tornado/ioloop.py
    _instance_lock = threading.Lock()
    background = [Explorer, googleIt, Research]
    _processes = []

    def __init__(self):
        super(App,self).__init__()
        print("Starting app")
        self.registerListener(self)
        self.queue = Queue(-1)
        self.tickTime = 1
        for s in self.background:
            self.addBackgroundProcess(s)
    def addBackgroundProcess(self,cls):
        c = cls()
        # register the class to the app
        # This allows events to transit between background processes
        c.registerListener(self)
        self._processes.append(c)
    def run(self):
        pass
    def addEvent(self,event):
        self.queue.put_nowait(event)
    def handle(self, event):
        if isinstance(event,Start):
            next_call = time.time()
            while True:
                self.emit(Tick(next_call))
                next_call = next_call + self.tickTime
                time.sleep(next_call - time.time())
        elif isinstance(event, Tick): #we do stuff on the queue
            self.process()
        else:
            self.addEvent(event) # reprocess the event, it's from background
    def process(self):
        print("ticking")
        try:
            event = self.queue.get_nowait()
        except Empty:
            return False
        self.emit(event) #we just emit the event, the thread will catch it
        log.info("processing event %s",event)

def start(app = None):
    log.info("starting background app")
    a = App()
    if app is not None:
        a = app
    a.emit(Start())
    return a

if __name__ == '__main__':
    print(start())