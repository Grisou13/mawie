# import tkinter
#
# from app.gui.components.mainFrame import MainFrame
# from app.gui.components.movie_frame import MovieFrame
# from app.gui.components.MovieList import MovieListFrame
# from app.models.Movie import Movie
# from app.models.File import File
#
#
# from app.gui.components.mainFrame import MainFrame
# from app.gui.components.movie_frame import MovieFrame
# from app.gui.components.MovieList import MovieListFrame
# from app.models.Movie import Movie
# from app.models.File import File
#
# from app.explorer.explorer import Explorer
#
# from app.helpers import SingletonMixin
# import weakref
# from app.gui.components.Search import SearchFrame
# from app.gui.components import GuiComponent
#
#
# class NotAComponent(Exception):
#     pass
#
#
# class Gui(SingletonMixin):
#
#     def __init__(self):
#
#         self.root_tkinter = tkinter.Tk()
#
#
#         self.root = tkinter.Tk()
#
#         self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur
#
#         self.components = weakref.WeakValueDictionary()
#
#         SearchFrame(self)
#
#         self.root = MainFrame(self)
#
#
#
#     def start(self):
#         self.root_tkinter.mainloop()
#
#
#     def addComponent(self, cls):
#         self.components[cls.__class__.__name__] = cls
#     def getShitDone(self):
#         self.addComponent(SearchFrame(self))
#         self.addComponent(Explorer(self))
#     def start(self):
#
#         self.root.mainloop()
#
#     def register_listener(self, cls):
#         if not isinstance(cls, GuiComponent):
#             raise NotAComponent("The class "+str(cls)+" should be extending GuiComponent")
#         self.listeners[cls] = 1
#
#     def dispatchAction(self, actionName, actionData):
#         for l in self.listeners.keys():
#             #print("from gui")
#             #print(l.__class__)
#             #print(id(l))
#             #print()
#             l.handleAction(actionName, actionData)
#
#     def requestAction(self, originClass, actionName):
#         for l in self.listeners.keys():
#             if isinstance(l, originClass): continue  # we don't request on the same object... would be pointless
#             originClass.handleAction("request_" + actionName, l.requestAction(actionName))
#
#
# if __name__ == '__main__':
#     g = Gui.instance()
#     g.start()
