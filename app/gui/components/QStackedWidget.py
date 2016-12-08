import copy
import sys
import weakref

from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt

from app.gui.components import GuiComponent
from app.gui.components.QExplorer import AddFilesWidget
from app.gui.components.QMovieListWidget import MovieListFrame
from app.gui.components.QMovieWidget import MovieFrame
from app.gui.components.QResearchWidget import  ResearchFrame
from app.gui.components.QExplorer import AddFilesWidget
from app.helpers import SingletonMixin



class ComponentArea(QStackedWidget,GuiComponent):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.gui = parent
        self.gui.register_listener(self)
        self.setMinimumSize(680, 700)
        self.initWidget()
    def initWidget(self):
        self.listMovie = MovieListFrame(self, self.gui)
        self.movie = MovieFrame(self, self.gui)
        self.explorer = AddFilesWidget(self, self.gui)

        self.addWidget(self.movie)
        self.addWidget(self.listMovie)
        self.addWidget(self.explorer)
        self.setCurrentWidget(self.listMovie)

    def handleAction(self, name, data):
        if name == "show-frame":
            print("showing frame "+str(data))
            if data is MovieFrame:
                self.setCurrentWidget(self.movie)
            elif data is MovieListFrame:
                self.setCurrentWidget(self.listMovie)


    def requestAction(self, name):
        pass

if __name__ == '__main__':
    from app.gui.Qgui import Gui

    Gui.start()