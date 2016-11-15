<<<<<<< develop
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
        listFrames = [MovieListFrame,MovieFrame]#list all frame that MainFrame have to display here
        self.frames = {}
        for F in listFrames:
            self.addFrame(F)

        self.showFrame("MovieListFrame")
    def addFrame(self,cls):
        frameName = (cls.__name__)
        frame = cls(parent=self, gui=self.gui)
        self.frames[frameName] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def showFrame(self,frameName):
        frame = self.frames[frameName]
        tkinter.Label(self,text="test")
        frame.tkraise()


    def handleAction(self,name,data):
        if name == "change_frame":
            self.showFrame(data)
        if name == "add_frame":
            self.addFrame(data)
        if name == 'search_selected':
            self.showFrame("MovieFrame")
        if name == 'list_result_search':
            self.showFrame("MovieListFrame")
    def requestAction(self,name):
        pass



=======
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
        listFrames = [MovieListFrame,MovieFrame]#list all frame that MainFrame have to display here
        self.frames = {}

        for F in listFrames:
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
        if name == 'list_result_search':
            self.showFrame("MovieListFrame")
    def requestAction(self,name):
        pass



>>>>>>> movie_frame -Change label value from french to english (réalisateur->director) -Display "-" if the movie attribut value is null MainFrame -change the name of the list of frame which was a bidon name Gui.py -comment lines which was used to debug
