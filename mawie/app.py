import threading
import time
from queue import Queue

from mawie.events import Eventable, Start
from mawie.helpers import Singleton



from mawie.events.app import *

from mawie.explorer.explorer import Explorer
from mawie.research.research import Research
from mawie.explorer.googleit import googleIt

class AppComponent(Eventable):
    pass


class App(Eventable, metaclass=Singleton):
    # based out of tornado ioloop https://github.com/tornadoweb/tornado/blob/master/tornado/ioloop.py
    _instance_lock = threading.Lock()
    background = [Explorer, googleIt, Research]
    _processes = []

    def __init__(self):
        super(App,self).__init__()
        print("Starting app")
        self.queue = Queue(-1)
        self.tickTime = .5
        for s in self.background:
            self.addBackgroundProcess(s)
    def addBackgroundProcess(self,cls):
        self._processes.append(cls())
    def run(self):
        pass
    def addEvent(self,event):
        self.queue.append(event)
    def handle(self, event):
        if isinstance(event,Start):
            next_call = time.time()
            while True:
                self.emit(Tick(next_call))
                next_call = next_call + self.tickTime
                time.sleep(next_call - time.time())
        if isinstance(event, Tick):
            self.process()
    def process(self):
        print("ticking")
        return True
        event = self.queue.pop()

def start():
    App().emit(Start())

if __name__ == '__main__':
    start()