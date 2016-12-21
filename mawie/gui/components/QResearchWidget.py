import logging

from PyQt5.QtWidgets import QLineEdit,QPushButton,QGridLayout

from mawie.events import Response
from mawie.events.gui import ShowMovieList
from mawie.events.search import SearchRequest, SearchResponse
from mawie.gui.components import GuiComponent
import qtawesome as qta
log = logging.getLogger("mawie")

class ResearchFrame(GuiComponent):
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

        #grid.addWidget(self.lbl,0,0)
        grid.addWidget(self.inputSearch,0,0,1,2)
        grid.addWidget(self.btnOk,0,2)

        self.setLayout(grid)
    def _showMovieList(self,*args,**kwargs):
        if self._textChangedFlag:
            self._forceFrameChange()
            self._textChangedFlag = False
    def _forceFrameChange(self):
        if len(self.inputSearch.text()) > 0:
            self.gui.emit(SearchRequest(self.inputSearch.text().lower()))
        self.gui.emit(ShowMovieList())


    def handle(self,event):
        #super().handle(event)
        if isinstance(event, Response) and isinstance(event.request, SearchRequest):
            log.info("-----EVENT RESPONSE AND REQUEST--------" + event.data)
            self.gui.emit(SearchResponse(event.request,event.data))
            self.gui.emit(ShowMovieList())
        elif isinstance(event, SearchResponse):
            log.info("-----EVENT SHOW FRAME--------" + event.data)
            self.gui.emit(SearchResponse(event.request, event.data))
            self.gui.emit(ShowMovieList())



if __name__ == '__main__':
    from mawie.gui.Qgui import start
    start()
