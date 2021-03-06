import os
import threading
import time
from queue import Queue, Empty, LifoQueue

from mawie.events import Eventable, Start, EventManager, Response, Quit, Request
from mawie.events.explorer import ExplorerParsingRequest
from mawie.events.search import SearchRequest
#from mawie.helpers import Singleton

from mawie.events.app import *

from mawie.explorer.explorer import Explorer
from mawie.research.research import Research
from mawie.explorer.googleit import GoogleIt
import logging

from mawie.updator import Updator

log = logging.getLogger(__name__)


class AppComponent(Eventable):
    pass


class App(EventManager):
    """
    Main app class. This runs all important process that handle data : searching, looking for files and indexing, etc...
    It is a special EventManager. It uses a queue to handle events.
    This allows for events to get around the app smoothly without python freaking out.

    Every listener (BackgroundProcess) added to this class will receive a special kind of emit.
    That emit will actually just add the event to the event queue.
    """
    # based out of tornado ioloop https://github.com/tornadoweb/tornado/blob/master/tornado/ioloop.py
    # doesn't work though
    _instance_lock = threading.Lock()
    background = [Explorer, GoogleIt, Research, Updator]
    _processes = []
    _running = False
    _lock = threading.Lock()

    def __init__(self):
        super().__init__()
        log.info("Starting background app")
        self.registerListener(self)
        self.queue = LifoQueue(-1)#Queue(-1)
        self.tickTime = .005 # clock the app at 200hz
        for s in self.background:
            self.addBackgroundProcess(s)

    def addBackgroundProcess(self, cls):
        c = cls()
        c.emit = self.addEvent
        # register the class to the app
        # This allows events to transit between background processes
        # c.registerListener(self)#bind the process, and the app together
        self.registerListener(c,"back")
        self._processes.append(c)

    def run(self):
        pass

    def addEvent(self, event, to = ""):
        with self._lock:
            self.queue.put([event,to],True,0)
            log.debug("queue size = %s",self.queue.qsize())

    def handle(self, event):
        if not isinstance(event,Tick):
            log.info("handling in bg process event : %s [event queue length = %s]",event,self.queue.qsize())
        if isinstance(event, Start):
            #next_call = time.time()
            self._running = True
            self.emit(event,"back") # emit to background processes
            while self._running:
                event.stopPropagate()
                self.emit(Tick(time.time()))
                #next_call = next_call - self.tickTime
                time.sleep(self.tickTime)
            for s in self._processes:
                s.emit(Quit())
            log.info("stopped background app")
        elif isinstance(event, Tick):  # we do stuff on the queue
            with self._lock:
                event_, to = self.process()
            if event_ is not False:
                if isinstance(event_,Response):
                    self.emit(event_,"front")
                elif isinstance(event,Request):
                    self.emit(event_, "back")
                else:
                    self.emit(event_,to)
        elif isinstance(event, Quit):
            self._running = False
            log.info("force quitting background app.... ")
            return
        elif isinstance(event, Response):
            self.emit(event,"front") #emit on the background listener only
        if isinstance(event,Request):
            if event.response is None:
                self.emit(event,"back")
            else:
                self.emit(event,"front")
    def process(self):
        try:
            eventDict = self.queue.get(True, 0)
            event = eventDict[0]
            to = eventDict[1]
            if to is "":
                to = "back"
            self.queue.task_done()
            log.info("processing event %s [timeout = %s, propagate = %s]", event, event.timeout,event.propogate)
            event.propogate = True
            return event, to
        except Empty:
            return False, ""


            # self.emit(event)


            # if isinstance(event,Response):#maybe it's a request with a response
            #     self.emit(event) #we just emit the event, the thread will catch it


def start(app=None):
    log.info("starting background app")

    if app is not None:
        a = app
    else:
        a = App()
        #a.addEvent(ExplorerParsingRequest(os.path.dirname(__file__)+"/../stubs/"))

    a.emit(Start())
    return a


if __name__ == '__main__':
    print(start())
