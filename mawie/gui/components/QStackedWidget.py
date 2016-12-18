import copy
import sys
import weakref

from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt

from mawie.events.gui import ShowFrame
from mawie.gui.components import GuiComponent
from mawie.gui.components.QAdvancedSearch import AdvancedSearch
#from mawie.gui.components.QExplorer import AddFilesWidget
from mawie.gui.components.QMovieListWidget import MovieListWidget
from mawie.gui.components.QMovieWidget import MovieWidget
from mawie.gui.components.QResearchWidget import  ResearchFrame
from mawie.gui.components.QExplorer import ExplorerWidget
from mawie.gui.components.QSettings import SettingsWidget
import logging
log = logging.getLogger("mawie")

class ComponentArea(QStackedWidget):
    def __init__(self, gui ,parent=None):
        super().__init__(parent)
        self.gui = gui
        self.setFixedSize(680, 700)
        self.widgetStore = {}
        self.currentChanged.connect(self.onCurrentChange)
        self.initWidget()

    def addWidget(self,widget):
        widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        widget.show()
        self.gui.registerListener(widget)
        super(ComponentArea, self).addWidget(widget)

    def onCurrentChange(self,index):
        w = self.widget(index)
        w.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        #self.adjustSize()
        #w.adjustSize()
        w.show()

    def addWidget(self,widget):
        log.info("adding widget %s",widget.__class__.__name__)
        if widget.__class__.__name__ not in self.widgetStore:
            widget.gui = self.gui
            widget.emit = lambda e: self.gui.emit(e)
            self.gui.registerListener(widget)
            self.widgetStore[widget.__class__.__name__] = widget
            #self.gui.register_listener(widget)
            super(ComponentArea,self).addWidget(widget)

    def initWidget(self):
        self.addWidget(AdvancedSearch(self))
        self.addWidget(ExplorerWidget(self))
        self.addWidget(MovieWidget(self))
        s = MovieListWidget(self)
        self.addWidget(s)
        self.addWidget(ExplorerWidget(self))
        self.addWidget(AdvancedSearch(self))
        self.setCurrentWidget(s)
        log.info("initialized : %s widgets",self.widgetStore)
    def handle(self,event):
        #super().handle(event)
        if isinstance(event, ShowFrame):
            if event.data.__class__.__name__ in self.widgetStore:
                event.stopPropagate()
                event.timeout = 0
                self.setCurrentWidget(self.widgetStore[event.data.__class__.__name__ ])

if __name__ == '__main__':
    from mawie.gui.Qgui import start
    start()