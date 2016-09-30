import tkinter
from app.gui.components.movie_frame import MovieFrame
from app.gui.components.test import Test

class Gui():
     root = tkinter.Tk()
     movieFrame= MovieFrame(root)
     search = Test(root,movieFrame)

