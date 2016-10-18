import tkinter
import tkinter.ttk
from tkinter.filedialog import askopenfilename, askdirectory

from app.explorer.explorer import Explorer
from app.gui.components import GuiComponent


class ExplorerFrame(tkinter.Frame, GuiComponent):
    def __init__(self, gui, *arg, **kwargs):
        self.gui = gui
        self.gui.register_listener(self)
        super(ExplorerFrame, self).__init__(gui.root, *arg, **kwargs)
        self.maxAllowedRatio = 10 # completly arbitrary, TODO fine tune this value
        try:
            self.explorer = Explorer(path="")
        except:
            pass
        self.grid()
        self.parsedList = tkinter.Listbox(self)
        self.nonParsedList = tkinter.Listbox(self)
        self.addDirectoryBtn = tkinter.Button(self)
        self.addDirectoryBtn.bind("<ButtonRelease-1>", self.addDirectory)
        self.gridElements()
    def gridElements(self):

        self.parsedList.grid(row=1, column=1)
        tkinter.ttk.Separator(self, orient=tkinter.HORIZONTAL).grid(row=2, padx=10, pady=2, columnspan=5,sticky="ew")
        self.nonParsedList.grid(row=3, column=1)
        self.addDirectoryBtn.grid(row=1, column=5)
    def addDirectory(self,event):
        try:

            self.parsedList.delete(0, tkinter.END)
            self.nonParsedList.delete(0, tkinter.END)
            directory = askdirectory(initialdir="/", mustexist=True)
            print(directory)
            movies = self.explorer.getMoviesIn(directory)
            for m in movies:
                pass
                #normally this should add to the parsed list the movie that have titles that are very far away from the original title,
                #otherwise they are added to the 'non-parsed' and then the user decides what to do with them
                #we use a levenstein funciton to do this
                """
                if leventsein(m["filename"], m["name"]) < self.maxAllowedRatio:
                    self.parsedList.insert(END,m["name"])
                else:
                    self.nonParsedList.insert(END,m["name"])

                #or the explorer does this
                if m["isParsed"]:
                    self.parsedList.insert(END,m["name"])
                else:
                    self.nonParsedList.insert(END,m["name"])
                """
        except Exception as e:
            self.gui.dispatchAction("widget-error",e)
            pass #something went wrong and should deal with it
    def requestAction(self, actionName):
        pass

    def handleAction(self, actionName, data):
        pass

if __name__ == '__main__':
    from app.gui.gui import Gui
    g = Gui.instance()
    g.addComponent(ExplorerFrame(g))
    g.start()