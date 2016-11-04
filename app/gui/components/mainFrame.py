import tkinter
from app.gui.components import GuiComponent
from app.gui.components.movie_frame import  MovieFrame
from app.gui.components.MovieList import MovieListFrame


class MainFrame(tkinter.Frame, GuiComponent):

    def __init__(self, gui,*args, **kwargs):
        self.gui = gui
        gui.register_listener(self)
        super(MainFrame,self).__init__(gui.root_tkinter)
        self.grid()
        test = [MovieListFrame,MovieFrame]#list all frame that MainFrame have to display here
        self.frames = {}
        for F in test:
            frameName = (F.__name__)
            frame = F(parent=self, gui=self.gui)
            self.frames[frameName] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.showFrame("MovieListFrame")


    def showFrame(self,frameName):
        frame = self.frames[frameName]
        tkinter.Label(self,text="test")
        frame.tkraise()


    def handleAction(self,name,data):
        if name == 'search_selected':
            self.showFrame("MovieFrame")
            self.gui.dispatchAction("update_movie_info", data)
    def requestAction(self,name):
        pass



