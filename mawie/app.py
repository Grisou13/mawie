import threading
import time
from queue import Queue, Empty

from mawie.events import Eventable, Start, EventManager, Response, Quit, Request
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
    _running = False
    def __init__(self):
        super(App,self).__init__()
        log.info("Starting background app")
        self.registerListener(self)
        self.queue = Queue(-1)
        self.tickTime = 1
        for s in self.background:
            self.addBackgroundProcess(s)
    def addBackgroundProcess(self,cls):
        c = cls()
        # register the class to the app
        # This allows events to transit between background processes
        c.registerListener(self)#bind the process, and the app together
        self.registerListener(c)
        self._processes.append(c)
    def run(self):
        pass
    def addEvent(self,event):
        event.timeout = 2 #allow it to cycle twice
        self.queue.put_nowait(event)
    def handle(self, event):
        if isinstance(event,Start):
            next_call = time.time()
            self._running = True
            while self._running:
                self.emit(Tick(next_call))
                next_call = next_call + self.tickTime
                time.sleep(next_call - time.time())
            for s in self._processes:
                s.emit(Quit())
            log.info("Stopping background app")
        elif isinstance(event, Tick): #we do stuff on the queue
            self.process()
        elif isinstance(event,Quit):
            self._running = False
            log.info("quitting background app.... ")
        elif isinstance(event, Response):
            self.addEvent(event) # reprocess the event, it's from background
    def process(self):
        log.info("ticking")
        log.info("queue length: %s", self.queue.qsize())
        try:
            event = self.queue.get_nowait()
        except Empty:
            return False
        log.info("processing event %s [timeout = %s]", event,event.timeout)

        self.emit(event)
        self.queue.task_done()

        # if isinstance(event,Response):#maybe it's a request with a response
        #     self.emit(event) #we just emit the event, the thread will catch it


def start(app = None):
    log.info("starting background app")
    a = App()
    if app is not None:
        a = app
    a.emit(Start())
    return a

if __name__ == '__main__':
    print(start())