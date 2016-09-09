# helper.py
import os
_dir = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.join(_dir,"../")
CACHE_PATH = os.path.join(BASE_PATH,".cache/")
DB_FILE = os.path.join(CACHE_PATH,'main.sqlite')
DB_PATH=r"sqlite:///"+DB_FILE