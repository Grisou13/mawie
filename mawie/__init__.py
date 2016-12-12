import sys
import os
import threading

if __name__ == '__main__':#TODO this is a complete hack, this should be fioxed or use relative imports
    sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
    sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import time
from queue import Queue

from mawie.events import Eventable, Start
from mawie.helpers import SingletonMixin



from mawie.events.app import *

class App(Eventable):
    # based out of tornado ioloop https://github.com/tornadoweb/tornado/blob/master/tornado/ioloop.py
    _instance_lock = threading.Lock()

    @staticmethod
    def instance():
        if not hasattr(App, "_instance"):
            with App._instance_lock:
                if not hasattr(App, "_instance"):
                    # New instance after double check
                    App._instance = App()
        return App._instance

    def __init__(self):
        super(App,self).__init__()
        self.queue = Queue()
        self.tickTime = 5
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
if __name__ == '__main__':
    App.instance().emit(Start())
