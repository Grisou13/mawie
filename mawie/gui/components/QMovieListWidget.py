import os

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QGridLayout,QListWidget,QListWidgetItem
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QRect,pyqtSignal

import mawie
from mawie.events import Response
from mawie.events.gui import SearchResults, ShowMovieList, ShowFrame, ShowMovieInfo
from mawie.events.search import SearchResult, SearchResponse, SearchRequest
from mawie.gui.components import GuiComponent, Downloader
from mawie.gui.components.QMovieWidget import MovieWidget
from mawie.gui.components.QPoster import QPoster
from mawie.models.Movie import Movie
from urllib import request
import asyncio
import logging
log = logging.getLogger("mawie")


class MovieListWidget(GuiComponent):

    def __init__(self,parent = None):
        super(MovieListWidget, self).__init__(parent)
        self.initFrame()
    # def showEvent(self, QShowEvent):
    #     super(MovieListFrame, self).showEvent(QShowEvent)
    #     self.updateWidgets(Research().search()) # execute search before showing widget
    def initFrame(self):
        self.createWidgets()
        self.show()

    def createWidgets(self):
        grid = QGridLayout(self)
        self.lstWidgets = QListWidget(self)
        grid.addWidget(self.lstWidgets)
        self.setLayout(grid)

    def updateWidgets(self,data):
        self.lstWidgets.clear()
        for film in data:
            try:
                log.info("---- NEW FILM -------- %s",film)
                item = QListWidgetItem(self.lstWidgets)
                itemW= ResultRow(self,film)
                item.setSizeHint(itemW.sizeHint())
                self.lstWidgets.setItemWidget(item, itemW)
                #itemW.show.connect(lambda x: self.clickedSee(film))
                itemW.btnSee.clicked.connect(lambda ignore, x=film: self.clickedSee(x))

            except Exception as e:
                log.info("ERROR WHILE UPDATING MOVIE LIST")
                log.info(e)
        log.info("List of widgets %s", len(self.lstWidgets))

    def clickedSee(self,film):
        self.emit(ShowFrame(MovieWidget.__name__,film))

    def handle(self, event):
        super().handle(event) #remember kids, always call super
        # if isinstance(event,ShowMovieList):
        #     event.stopPropagate()
        #     self.emit(ShowFrame(self))
        # if isinstance(event,SearchResponse):
        #     log.info("-------------- UPDATING LIST OF MOVIES ----------------")
        #     self.updateWidgets(event.data)
        #     #self.emit(ShowFrame(self))
        if isinstance(event, Response) and isinstance(event.request, SearchRequest):
            log.info("-------------- UPDATING LIST OF MOVIES ----------------")
            self.updateWidgets(event.data)
            event.stopPropagate()
            #self.emit(ShowFrame(self))
        if isinstance(event,ShowMovieList):
            self.emit(ShowFrame(self))
    #     if isinstance(event, SearchResponse):
    #         self.updateWidgets(event.data)

class ResultRow(QWidget):

    show = pyqtSignal()
    def __init__(self,parent,data):
        super(ResultRow,self).__init__(parent)
        self.film = data
        self.initRow(data)

    def initRow(self,data):
        self.createWidgets(data)

    def createWidgets(self,data):
        grid = QGridLayout(self)
        lblImg = QPoster(self, data.poster)
        #self.importPosterFilm(data.poster)
        if data.name is not None:
            if data.genre is not None:
                lblTitle = QLabel(data.name + "(" + data.genre + ")", self)
            else:
                lblTitle = QLabel("Title: " + data.name, self)
        else:
            lblTitle = QLabel("Title: -", self)
        if data.actors is not None:
            lblActors = QLabel("Actor(s): "+data.actors,self)
        else:
            lblActors = QLabel("Actors(s): -",self)
        if data.directors is not None:
            lblRating = QLabel("IMDb Rating: "+data.rate,self)
        else:
            lblRating = QLabel("IMDb Rating: -", self)
        self.btnSee = QPushButton("See info",self)

        lblTitle.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        lblActors.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        lblRating.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lblActors.setWordWrap(True)
        lblTitle.setWordWrap(True)
        lblRating.setWordWrap(True)

        grid.addWidget(lblImg,0,0,3,2)
        grid.addWidget(lblImg,0,0,3,2)
        grid.addWidget(lblTitle, 0, 2)
        grid.addWidget(lblRating, 1, 2)
        grid.addWidget(lblActors, 2, 2)
        grid.addWidget(self.btnSee, 1,3)
        self.setLayout(grid)

if __name__ == '__main__':
    from mawie.gui.Qgui import start
    start()