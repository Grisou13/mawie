# helper.py
import os
import socket

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap

from mawie.gui.components import Downloader

_dir = os.path.dirname(os.path.realpath(__file__))

BASE_PATH = os.path.join(_dir,"../")
CACHE_PATH = os.path.join(BASE_PATH,".cache/")
DB_FILE = os.path.join(CACHE_PATH,'main.sqlite')
DB_PATH=r"sqlite:///"+DB_FILE


import threading
#http://stackoverflow.com/questions/2682745/how-to-create-a-constant-in-python
def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)
# Based on tornado.ioloop.IOLoop.instance() approach.
# See https://github.com/facebook/tornado
#tooken from https://gist.github.com/werediver/4396488
class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if SingletonMixin._instance is None:
            with SingletonMixin._lock:
                if SingletonMixin._instance is None:
                    SingletonMixin._instance = super(SingletonMixin, cls).__new__(cls)
        print(SingletonMixin._instance)
        return SingletonMixin._instance


def checkInternetConnexion():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect(("google.com", 80)) #if the computer doesn't have a dns and can't handle google... don't know what else to do man
        return True
    except Exception as e:
        return False
if __name__ == '__main__':
    class A(SingletonMixin): pass
    class B(SingletonMixin): pass
    a,b = A(), B()
    a1,b1 = A(),B()
    print(a)
    print(b)
    print(a1)
    print(b1)