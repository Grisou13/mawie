import tkinter
import tkinter.ttk
from app.gui.components import GuiComponent


class ExplorerFrame(tkinter.Frame, GuiComponent):
    def __init__(self, gui, *arg, **kwargs):
        self.gui = gui
        self.gui.register_listener(self)
        super(ExplorerFrame, self).__init__(gui.root, *arg, **kwargs)
        self.grid()
        self.list = tkinter.Listbox()

    def requestAction(self, actionName):
        pass

    def handleAction(self, actionName, data):
        pass

if __name__ == '__main__':
    from app.gui.gui import Gui
    g = Gui.instance()
    g.addComponent(ExplorerFrame(g))
    g.start()