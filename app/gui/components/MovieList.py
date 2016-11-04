import tkinter
from app.gui.components import GuiComponent



class MovieListFrame(tkinter.Frame, GuiComponent):
    def __init__(self, parent, gui, *arg, **kwargs):
        self.parent= parent
        self.gui =gui
        gui.register_listener(self)
        super(MovieListFrame, self).__init__(parent)
        self.grid()
        self.createWidget()

    def createWidget(self):
        bgFrame = "#1E1E1F"
        colorFont = "#CBC9CF"
        btnColor = "#191919"
        lstColor="#191919"
        lstSelectColor="#39393B"
        sizeFontInfoFilm = 11
        lengthMaxLbl = 500
        self.lblTitle= tkinter.Label(self, text="test").grid()

        self.btnChange = tkinter.Button(self,text="CHANGE FRAME",command=lambda : self.gui.dispatchAction("test","")).grid()

    def handleAction(self, name, data):
        pass


    def requestAction(self, name):
        pass


