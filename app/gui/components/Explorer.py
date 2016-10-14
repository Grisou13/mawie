import tkinter
import tkinter.ttk
from app.gui.components import GuiComponent


class ExplorerFrame(tkinter.Frame,GuiComponent):
    def __init__(self, gui, *arg, **kwargs):
        self.gui = gui
        self.gui.register_listener(self)
        super(ExplorerFrame, self).__init__(gui.root, *arg, **kwargs)
        self.grid()
        self.list = tkinter.Listbox()
        self.list.pack()

    def requestAction(self, actionName):
        pass

    def handleAction(self, actionName, data):
        pass