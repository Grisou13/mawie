import os
import tkinter
import tkinter.ttk
from tkinter.filedialog import askopenfilename, askdirectory

from app.explorer.explorer import Explorer
from app.gui.components import GuiComponent

#must be redone with Qt
class ExplorerFrame(tkinter.Frame, GuiComponent):
    def __init__(self, gui, *arg, **kwargs):
        self.gui = gui
        self.gui.register_listener(self)
        super(ExplorerFrame, self).__init__(gui.root, *arg, **kwargs)
        self.maxAllowedRatio = 10 # completly arbitrary, TODO fine tune this value
        self.explorer = Explorer()

        self.grid()
        self.parsedList = tkinter.Listbox(self, selectmode=tkinter.EXTENDED)
        self.nonParsedList = tkinter.Listbox(self, selectmode=tkinter.EXTENDED)
        self.toNonParsed = tkinter.Button(self,text="->",command=self._moveListToNonParsed)
        self.toParsed = tkinter.Button(self,text="<-",command=self._moveListToParsed)
        self.addDirectoryBtn = tkinter.Button(self,{"text":"add dir"})
        self.addDirectoryBtn.bind("<ButtonRelease-1>", self.addDirectory)
        self.commitBtn = tkinter.Button(self,text="commit",command=self._commitFiles)

        #just to test things out
        self.r = tkinter.StringVar()
        self.r.set(self.explorer.maxRatio)
        w = tkinter.Scale(from_=100, to=0, resolution=0.1,variable = self.r)
        w.grid(column = 5,row=1)
        self.explorer.maxRatio = float(self.r.get())
        w.bind("<ButtonRelease-1>",lambda x : self.parseDirectory(self.explorer.path))
        self.gridElements()
    def gridElements(self):
        self.parsedList.grid(row=1, column=1,rowspan=2)
        self.toNonParsed.grid(row=2,column=2)
        self.toParsed.grid(row=1,column=2)
        self.nonParsedList.grid(row=1, column=3,rowspan=2)
        tkinter.ttk.Separator(self, orient=tkinter.HORIZONTAL).grid(row=3, padx=10, pady=2, columnspan=5,sticky="ew")
        self.addDirectoryBtn.grid(row=4, column=4)
        self.commitBtn.grid(row=4,column=2)
    def _moveListToNonParsed(self):
        pass
    def _moveListToParsed(self):
        print(self.explorer.parsedFiles)
        print("moving lists eh")
        print(self.explorer.nonParsedFiles)
    def _commitFiles(self):
        print("commiting files")
        print(self.explorer.parsedFiles)
        self.explorer.commit()
    def parseDirectory(self,d):
        _, parsed,not_parsed = self.explorer.getFolderContent(os.path.normpath(d))
        print("List lengths \n parsed : ")
        print(len(parsed))
        print("not parsed : ")
        print(len(not_parsed))
        for m in parsed:
            self.parsedList.insert(tkinter.END, m["title"])
        for m in not_parsed:
            self.nonParsedList.insert(tkinter.END, m["title"])
    def addDirectory(self,event):
        self.parsedList.delete(0, tkinter.END)
        self.nonParsedList.delete(0, tkinter.END)
        directory = askdirectory(initialdir=os.getcwd(), mustexist=True)
        print(directory)
        if directory is None :
            return #user selected nothing
        self.parseDirectory(directory)

    def requestAction(self, actionName):
        pass

    def handleAction(self, actionName, data):
        if actionName == "parse-directory":
            self.parseDirectory(data)

if __name__ == '__main__':
    from app.gui.gui import Gui
    g = Gui.instance()
    g.addComponent(ExplorerFrame(g))
    g.dispatchAction("parse-directory","../../../stubs/FILM_a_trier")
    g.start()