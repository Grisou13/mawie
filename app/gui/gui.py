import tkinter

from app.gui.components.Search import SearchFrame
from app.helpers import SingletonMixin


class Gui(SingletonMixin):
    root = tkinter.Tk()
    search = SearchFrame(root)

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    g = Gui.instance()
    g.start()
