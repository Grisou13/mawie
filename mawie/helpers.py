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
LOG_PATH = os.path.join(BASE_PATH,"logs")

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
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
"""
Singelton decorator
"""
def singleton(class_):
  class class_w(class_):
    _instance = None
    def __new__(class_, *args, **kwargs):
      if class_w._instance is None:
          class_w._instance = super(class_w,
                                    class_).__new__(class_,
                                                    *args,
                                                    **kwargs)
          class_w._instance._sealed = False
      return class_w._instance
    def __init__(self, *args, **kwargs):
      if self._sealed:
        return
      super(class_w, self).__init__(*args, **kwargs)
      self._sealed = True
  class_w.__name__ = class_.__name__
  return class_w

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