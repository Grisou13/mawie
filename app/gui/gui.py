import tkinter

from app.helpers import SingletonMixin
import weakref
from app.gui.components.Search import SearchFrame
from app.gui.components import GuiComponent


class NotAComponent(Exception):
    pass


class Gui(SingletonMixin):

    def __init__(self):
        self.root = tkinter.Tk()

        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur
        SearchFrame(self)

    def start(self):
        self.root.mainloop()

    def register_listener(self, cls):
        if not isinstance(cls, GuiComponent):
            raise NotAComponent("The class "+str(cls)+" should be extending GuiComponent")
        self.listeners[cls] = 1

    def dispatchAction(self, actionName, actionData):
        for l in self.listeners.keys():
            l.handleAction(actionName, actionData)

    def requestAction(self, originClass, actionName):
        for l in self.listeners.keys():
            if isinstance(l, originClass): continue  # we don't request on the same object... would be pointless
            originClass.handleAction("request_" + actionName, l.requestAction("request_" + actionName))


if __name__ == '__main__':
    g = Gui.instance()
    g.start()
