# helper.py
import os
_dir = os.path.dirname(os.path.realpath(__file__))

BASE_PATH = os.path.join(_dir,"../")
CACHE_PATH = os.path.join(BASE_PATH,".cache/")
DB_FILE = os.path.join(CACHE_PATH,'main.sqlite')
DB_PATH=r"sqlite:///"+DB_FILE


import threading


# Based on tornado.ioloop.IOLoop.instance() approach.
# See https://github.com/facebook/tornado
#tooken from https://gist.github.com/werediver/4396488
class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()#object.__new__(cls)
        return cls.__singleton_instance