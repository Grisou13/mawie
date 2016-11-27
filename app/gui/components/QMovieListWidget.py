import os

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QGridLayout,QListWidget,QListWidgetItem
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QRect,pyqtSignal
from app.gui.components import GuiComponent, Downloader
from app.models.Movie import Movie
from urllib import request
import asyncio

class MovieListFrame(QWidget, GuiComponent):

    def __init__(self,parent=None,gui=None):
        super().__init__(parent)
        self.gui = gui
        self.gui.register_listener(self)

        self.initFrame()

    def initFrame(self):
        self.createWidgets()
        self.show()
    def createWidgets(self):
        grid = QGridLayout()

        self.listWidgets = QListWidget(self)
        self.listWidgets.setMinimumSize(670,700)
        self.updateWidgets(Movie.query())
        # for film in Movie.query():
        #     item = QListWidgetItem(self.listWidgets)
        #     itemW= ResultRow(self,film,self.gui)
        #     item.setSizeHint(itemW.sizeHint())
        #     self.listWidgets.setItemWidget(item, itemW)

        self.setLayout(grid)
    def updateWidgets(self,data):
        self.listWidgets.clear()
        for film in data:
            t =film
            try:
                item = QListWidgetItem(self.listWidgets)
                itemW= ResultRow(self,film,self.gui)
                item.setSizeHint(itemW.sizeHint())
                self.listWidgets.setItemWidget(item, itemW)
                itemW.btnSee.clicked.connect(lambda ignore, x = film : self.clickedSee(x))

            except Exception as e:
                print(e)

    def clickedSee(self,film):
        self.gui.dispatchAction("show-info-film",film)
    def handleAction(self,name,data):
        if name == "search-results":
            self.updateWidgets(data)
    def requestAction(self,name):
        pass

class ResultRow(QWidget):
    selectedMovie = pyqtSignal()

    def __init__(self,parent,data,gui):
        super().__init__(parent)
        # self.gui = gui
        # self.gui.register_listener(self)
        self.film = data
        self.downloader = Downloader()
        self.initRow(data)
        #self.setGeometry(QRect(0,0,700,160))
        #self.setMinimumSize(650,160)
        #self.setSizePolicy(650,160)

    def initRow(self,data):
        self.createWidgets(data)
        #self.show()

    def createWidgets(self,data):
        grid = QGridLayout()

        lblImg = QLabel(self)
        # if data.poster is not None:
        #     self.importPosterFilm(data.poster)
        # else :
        self.importPosterFilm(data.poster)
        #lblImg.setPixmap(poster)
        self.image = lblImg
        if data.name is not None:
            if data.genre is not None:
                lblProducer = QLabel(data.name+"("+data.genre+")", self)
            else:
                lblProducer = QLabel("Title: " + data.name, self)
        else:
            lblProducer = QLabel("Title: -", self)
        if data.actors is not None:
            lblActors = QLabel("Actor(s): "+data.actors,self)
        else:
            lblActors = QLabel("Actors(s): -",self)
        if data.directors is not None:
            lblRating = QLabel("IMDb Rating: "+data.rate,self)
        else:
            lblRating = QLabel("IMDb Rating: -", self)
        self.btnSee = QPushButton("See info",self)

        lblActors.setFixedWidth(400)
        lblProducer.setFixedWidth(400)
        lblRating.setFixedWidth(400)

        lblActors.setWordWrap(True)
        lblProducer.setWordWrap(True)
        lblRating.setWordWrap(True)

        lblImg.setMinimumSize(100,160)
        lblImg.setScaledContents(True)  # fit image to label

        grid.addWidget(lblImg,0,0,3,2)


        grid.addWidget(lblImg,0,0,3,2)
        grid.addWidget(lblProducer,0,2)
        grid.addWidget(lblRating, 1, 2)
        grid.addWidget(lblActors, 2, 2)
        grid.addWidget(self.btnSee, 0, 3,3,2)



        self.setLayout(grid)

    def seeFilm(self):
        print(self.film.name)

    def importPosterFilm(self,path=None):
        downloader = self.downloader
        if path is None:
            path = "qrc:///no-poster"
            # self.image.setPixmap(QPixmap(":/no-poster"))
            # return True
            # if os.path.exists(os.path.join(os.path.realpath(__file__),"../../../../",".cache","noPoster.jpg")):
            #     path = "file://"+os.path.realpath(os.path.join(os.path.realpath(__file__),"../../../../",".cache","noPoster.jpg"))
            # elif os.path.exists(os.path.join(os.path.realpath(__file__),"../","noPoster.jpg")):
            #     path = "file://"+os.path.realpath(os.path.join(os.path.realpath(__file__),"../","noPoster.jpg"))

        try:
            path = QUrl(path)
            # html = request.urlopen(path)
            # data = html.read()
            # image.loadFromData(data)
            downloader.downloaded.connect(self.updateImage)
            downloader.doDownload(path)
        except request.URLError: #in case there isn't the internet or the url gives 404 error or bad url
            print("a problem with the connection or the url has occurred")

    def updateImage(self):
        image = QPixmap()
        image.loadFromData(self.downloader.downloadedData())
        self.image.setPixmap(image)
if __name__ == '__main__':
    from app.gui.Qgui import Gui
    Gui.start()