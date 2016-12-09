import os

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QGridLayout,QListWidget,QListWidgetItem
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QRect,pyqtSignal

import mawie
from mawie.gui.components import GuiComponent, Downloader
from mawie.gui.components.QPoster import QPoster
from mawie.models.Movie import Movie
from urllib import request
import asyncio

from mawie.research.research import Research


class MovieListFrame(QWidget, GuiComponent):

    def __init__(self,parent=None,gui=None):
        super().__init__(parent)
        parent.addWidget(self)
        parent.setCurrentWidget(self)
        self.gui = gui
        self.gui.register_listener(self)
        self.initFrame()
    # def showEvent(self, QShowEvent):
    #     super(MovieListFrame, self).showEvent(QShowEvent)
    #     self.updateWidgets(Research().search()) # execute search before showing widget
    def initFrame(self):
        self.createWidgets()
        self.show()
    def createWidgets(self):
        grid = QGridLayout()
        self.listWidgets = QListWidget(self)
        self.listWidgets.setMinimumSize(670,700)

        # for film in Movie.query():
        #     item = QListWidgetItem(self.listWidgets)
        #     itemW= ResultRow(self,film,self.gui)
        #     item.setSizeHint(itemW.sizeHint())
        #     self.listWidgets.setItemWidget(item, itemW)

        self.setLayout(grid)
    def updateWidgets(self,data):
        self.listWidgets.clear()
        for film in data:
            try:
                item = QListWidgetItem(self.listWidgets)
                itemW= ResultRow(self,film,self.gui)
                item.setSizeHint(itemW.sizeHint())
                self.listWidgets.setItemWidget(item, itemW)
                #itemW.show.connect(lambda x: self.clickedSee(film))
                itemW.btnSee.clicked.connect(lambda ignore, x = film : self.clickedSee(x))

            except Exception as e:
                print(e)

    def clickedSee(self,film):
        self.gui.dispatchAction("show-info-film",film)
    def handleAction(self,name,data):
        if name == "show-movie-list-frame":
            self.gui.dispatchAction("show-frame",self)
        if name == "search-results":
            self.updateWidgets(data)
            self.gui.dispatchAction("show-frame",self)
    def requestAction(self,name):
        pass

class ResultRow(QWidget):
    show = pyqtSignal()

    def __init__(self,parent,data,gui):
        super(ResultRow,self).__init__(parent)
        self.film = data
        self.initRow(data)
        #self.setGeometry(QRect(0,0,700,160))
        #self.setMinimumSize(650,160)
        #self.setSizePolicy(650,160)
        #self.setMinimumHeight(200)
    def initRow(self,data):
        self.createWidgets(data)
        #self.show()

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
        #self.btnSee.clicked.connect(lambda x : self.show.emit(self.film))
        lblActors.setFixedWidth(400)
        lblTitle.setFixedWidth(400)
        lblTitle.setMinimumHeight(70)
        lblRating.setFixedWidth(400)

        lblActors.setWordWrap(True)
        lblTitle.setWordWrap(True)
        lblRating.setWordWrap(True)

        grid.addWidget(lblImg,0,0,3,2)
        grid.addWidget(lblImg,0,0,3,2)
        grid.addWidget(lblTitle, 0, 2)
        grid.addWidget(lblRating, 1, 2)
        grid.addWidget(lblActors, 2, 2)
        grid.addWidget(self.btnSee, 0, 3,3,2)
        self.setLayout(grid)
    def seeFilm(self):
        print(self.film.name)
if __name__ == '__main__':
    from mawie.gui.Qgui import Gui
    Gui.start()