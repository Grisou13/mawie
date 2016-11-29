import sys
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QPushButton,QGridLayout
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt
from PyQt5.uic.properties import QtGui, QtCore

from app.gui.components import GuiComponent
from app.gui.components.QMovieListWidget import MovieListFrame
from app.research.research import Research
import re

class ResearchFrame(QWidget, GuiComponent):
    def __init__(self,parent):
        super().__init__(parent)
        self.gui = parent
        self.gui.register_listener(self)
        self.search = Research()
        self.initFrame()
        self._textChangedFlag = False
    def initFrame(self):
        self.createWidget()
        self.show()
    def refreshSearch(self,text):
        if text is not "":
            self._textChangedFlag = True
            results = self.search.search(self.inputSearch.text().lower())
            self.gui.dispatchAction("search-results",results)
            #self.model.setStringList([str(x) for x in results])
        else:
            self._textChangedFlag = False
            self.gui.dispatchAction("show-initial-list")
    def createWidget(self):
        grid = QGridLayout(self)
        self.lbl = QLabel("Please enter a research", self)
        self.inputSearch = QLineEdit(self)
        self.inputSearch.setFixedWidth(200)
        self.completer = QCompleter()
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        #self.inputSearch.setCompleter(self.completer)
        self.inputSearch.textChanged.connect(self.refreshSearch)
        self.inputSearch.editingFinished.connect(self._showMovieList)
        self.model = QStringListModel()
        #self.completer.setModel(self.model)
        #self.model.setStringList([])
        self.btnOk = QPushButton("Launch the research", self)
        self.btnOk.clicked.connect(self._forceFrameChange)
        grid.addWidget(self.lbl,0,0)
        grid.addWidget(self.inputSearch,0,1)
        grid.addWidget(self.btnOk,0,2)

        self.setLayout(grid)
    def _showMovieList(self,*args,**kwargs):
        if self._textChangedFlag:
            print("editing finished showing movie list")
            self._forceFrameChange()
            self._textChangedFlag = False
    def _forceFrameChange(self):
        self.gui.dispatchAction("show-frame", MovieListFrame)
    def handleAction(self, actionName, data):
       pass
    def requestAction(self,name):
        pass
if __name__ == '__main__':
    from app.gui.Qgui import Gui
    Gui.start()
# import sys
#
# from PyQt5.QtCore import QStringListModel
# from PyQt5.QtWidgets import QCompleter
# from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QVBoxLayout
# from PyQt5.QtGui import QPixmap,QFont
# from PyQt5.QtCore import QRect,Qt
# from PyQt5.uic.properties import QtGui
#
# from app.research.research import Research
#
# import re
#
# class ResearchFrame(QWidget):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.search = Research()
#         self.initFrame()
#
#     def initFrame(self):
#         self.createWidget()
#         self.show()
#     def refreshSearch(self):
#         self.model.setStringList(self.search.search(self.inputSearch.text().lower()))
#     def createWidget(self):
#         grid = QGridLayout(self)
#         self.lbl = QLabel("Please enter a resarch", self)
#         self.inputSearch = QLineEdit(self)
#         self.inputSearch.setFixedWidth(300)
#         self.completer = QCompleter()
#
#         self.inputSearch.setCompleter(self.completer)
#         self.inputSearch.textChanged.connect(self.refreshSearch)
#
#         self.model = QStringListModel()
#         self.completer.setModel(self.model)
#         self.model.setStringList([])
#         self.btnOk = QPushButton("Launch the research", self)
#         grid.addWidget(self.lbl,0,0)
#         grid.addWidget(self.inputSearch,0,1)
#         grid.addWidget(self.btnOk,0,2)
#
#         self.setLayout(grid)
# if __name__ == '__main__':
#     from app.gui.Qgui import Gui
#     Gui.start()
