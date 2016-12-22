import logging

import qtawesome as qta
from PyQt5.QtWidgets import QLineEdit,QPushButton,QGridLayout

from mawie.events import Response
from mawie.events.search import SearchRequest, SearchResponse
from mawie.events.gui import ShowFrame
from mawie.gui.components import GuiComponent
from mawie.models import Movie
log = logging.getLogger("mawie")

class ResearchWidget(GuiComponent):
    def __init__(self,parent = None):
        super().__init__(parent)
        self._textChangedFlag = False
        self.initFrame()

    def initFrame(self):
        self.createWidget()
        self.show()
    def refreshSearch(self,text):
        if text is not "":
            self._textChangedFlag = True
            self.gui.emit(SearchRequest(self.inputSearch.text().lower()))
            #self._showMovieList()
        else:
            self._textChangedFlag = False
    def createWidget(self):
        grid = QGridLayout(self)
        #self.lbl = QLabel("Please enter a research", self)
        self.inputSearch = QLineEdit(self)
        self.btnAllMovies = QPushButton("All the movies")
        self.btnAllMovies.setMaximumWidth(100)
        self.btnAllMovies.clicked.connect(self._displayAllMovies)

        #self.inputSearch.setFixedWidth(200)
        #self.completer = QCompleter()
        #self.completer.setCompletionMode(QCompleter.PopupCompletion)
        #self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        #self.inputSearch.setCompleter(self.completer)
        self.inputSearch.textChanged.connect(self.refreshSearch)
        self.inputSearch.editingFinished.connect(self._showMovieList)
        #self.model = QStringListModel()
        #self.completer.setModel(self.model)
        #self.model.setStringList([])
        icon = qta.icon('fa.search',color="white")
        self.btnOk = QPushButton(self)
        self.btnOk.setIcon(icon)
        self.btnOk.clicked.connect(self._forceFrameChange)
        grid.addWidget(self.btnAllMovies, 0, 0)
        grid.addWidget(self.inputSearch, 0, 1)
        grid.addWidget(self.btnOk, 0, 2)

        self.setLayout(grid)
    def _displayAllMovies(self):
        self.gui.emit(SearchRequest(""))
        self.gui.emit(ShowFrame('MovieListWidget'))

    def _showMovieList(self,*args,**kwargs):
        if self._textChangedFlag:
            self._forceFrameChange()
            self._textChangedFlag = False
    def _forceFrameChange(self):
        if len(self.inputSearch.text()) > 0:
            self.gui.emit(SearchRequest(self.inputSearch.text().lower()))
        self.gui.emit(ShowFrame('MovieListWidget'))

        #self.gui.emit(ShowMovieList())


    def handle(self,event):
        #super().handle(event)
        if isinstance(event, Response) and isinstance(event.request, SearchRequest):
            log.info("-----EVENT RESPONSE AND REQUEST--------" + event.data)
            self.gui.emit(SearchResponse(event.request,event.data))
            self.gui.emit(ShowFrame('MovieListWidget'))
            #self.gui.emit(ShowMovieList())
        elif isinstance(event, SearchResponse):
            log.info("-----EVENT SHOW FRAME--------" + event.data)
            self.gui.emit(SearchResponse(event.request, event.data))
            self.gui.emit(ShowFrame('MovieListWidget'))

if __name__ == '__main__':
    from mawie.gui import start
    start()