import app.main
import sys
from app.explorer.explorer import *

def run():
    app = main.App()

    #only for test the explorer class with original path (mawie file)

    # coding=utf-8
    explorer = Explorer("stubs/FILM_a_trier")
    explorer.writeContentInJson(explorer.nameParsing(explorer.getFolderContent()))
    print("stuff is done")
