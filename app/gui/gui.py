import tkinter

from app.gui.components.Search import SearchWidget
from app.helpers import SingletonMixin

class Gui(SingletonMixin):
     root = tkinter.Tk()
     search = SearchWidget(root)
     def start(self):
          self.root.mainloop()
if __name__ == '__main__':
    g = Gui.instance()
    g.start()
