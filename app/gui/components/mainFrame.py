import tkinter
from app.gui.components import GuiComponent
from app.gui.components.movie_frame import  MovieFrame
from app.gui.components.Search import SearchFrame
from app.gui.gui import Gui



class MainFrame(tkinter.Frame,GuiComponent):

    def __init__(self, gui,*args, **kwargs):
        super(tkinter.Frame).__init__(gui.root)
        self.gui = gui

        componentFrames=[MovieFrame,SearchFrame]
        self.frames = {}
        for F in componentFrames:
            frameName = F.__name__
            frame = F(parent=self, controller=self.gui.root)
            self.frames[frameName] = frame
            frame.grid(row=1,column=1)
        self.showFrame("MovieFrame")

    def showFrame(self,frameName):
        frameToShow= self.frames[frameName]
        frameToShow.tkraise()
    def handleAction(self,name,data):
        pass
    def requestAction(self,name):
        pass

if __name__ == '__main__':
    gui = Gui()
    frame=MainFrame(gui)
    frame.mainloop()


