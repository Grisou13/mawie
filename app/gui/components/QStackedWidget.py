import copy
import sys
import weakref

from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt

from app.gui.components import GuiComponent
from app.gui.components.QAdvancedSearch import AdvancedSearch
#from app.gui.components.QExplorer import AddFilesWidget
from app.gui.components.QMovieListWidget import MovieListFrame
from app.gui.components.QMovieWidget import MovieFrame
from app.gui.components.QResearchWidget import  ResearchFrame
from app.helpers import SingletonMixin



class ComponentArea(QStackedWidget,GuiComponent):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.gui = parent
        self.gui.register_listener(self)
        self.setFixedSize(680, 700)

        self.currentChanged.connect(self.onCurrentChange)
        self.initWidget()

    def addWidget(self,widget):
        widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        super(ComponentArea, self).addWidget(widget)
    def onCurrentChange(self,index):
        w = self.widget(index)
        w.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
        self.adjustSize()
        w.adjustSize()
        w.show()

    def initWidget(self):
        MovieFrame(self, self.gui)
        MovieListFrame(self, self.gui)
        s = AdvancedSearch(self,self.gui)
        self.setCurrentWidget(s)
        # self.listMovie = MovieListFrame(self, self.gui)
        # self.movie = MovieFrame(self, self.gui)

        # self.addWidget(self.movie)
        # self.addWidget(self.listMovie)
        # self.setCurrentWidget(self.listMovie)
    def handleAction(self, name, data):
        if name == "show-frame":
            print(hex(id(data)))
            print(self.indexOf(data))
            if self.indexOf(data) is not -1:
                self.setCurrentWidget(data)
                # self.currentWidget().show()
                # self.currentWidget().setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
                # self.currentWidget().adjustSize()


    def requestAction(self, name):
        pass

if __name__ == '__main__':
    from app.gui.Qgui import Gui

    Gui.start()
