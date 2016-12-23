import logging
from PyQt5 import Qt
from cmath import rect

from PyQt5.QtCore import QRect
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QGridLayout,QListWidget,QListWidgetItem

from mawie.events import Response
from mawie.events.gui import ShowFrame, ShowSearch
from mawie.events.search import SearchRequest
from mawie.gui.components import GuiComponent
from mawie.gui.components.QMovieWidget import MovieWidget
from mawie.gui.components.QPoster import QPoster
from mawie.models.Movie import Movie

log = logging.getLogger("mawie")


class MovieListWidget(GuiComponent):

    def __init__(self,parent = None):
        """
        This widget displays a list of film

        :param parent: parent of the widget
        :type parent: QWidget

        """
        super(MovieListWidget, self).__init__(parent)

        self.createWidgets()
        self.updateWidgets(Movie.query())

    # def showEvent(self, QShowEvent):
    #     super(MovieListFrame, self).showEvent(QShowEvent)
    #     self.updateWidgets(Research().search()) # execute search before showing widget


    def onShowFrame(self):
        self.emit(ShowSearch())

    def createWidgets(self):
        grid = QGridLayout(self)
        self.lstWidgets = QListWidget(self)
        #self.btnGoToExplorer = QPushButton("Go to explorer",self)
        #grid.addWidget(self.btnGoToExplorer,0,0)
        self.lblNoFilm = QLabel("There is no film")
        font = QFont('',15)
        self.lblNoFilm.setFont(font)
        grid.addWidget(self.lblNoFilm,0,0,1,1, Qt.Qt.AlignCenter)
        grid.addWidget(self.lstWidgets,0,0)
        self.setLayout(grid)

        # if Movie.query().count() >0:
        #     self.lstWidgets.setVisible(True)
        #     self.btnGoToExplorer.setVisible(False)
        # else:
        #     self.btnGoToExplorer.setVisible(True)
        #     self.lstWidgets.setVisible(False)


    def updateWidgets(self,data):
        """
        update the list with the data parameter
        :param data:
        :type: list of movies model
        :return:
        """
        hasFilm = False
        self.lstWidgets.clear()

        for film in data:
            hasFilm = True
            try:
                item = QListWidgetItem(self.lstWidgets)
                itemW= ResultRow(self,film)
                item.setSizeHint(itemW.sizeHint())
                self.lstWidgets.setItemWidget(item, itemW)
                #itemW.show.connect(lambda x: self.clickedSee(film))
                itemW.btnSee.clicked.connect(lambda ignore, f=film: self.clickedSee(f))

            except Exception as e:
                log.info("ERROR WHILE UPDATING MOVIE LIST")
                log.info(e)
        if hasFilm is True:
            self.lblNoFilm.setVisible(False)
        else:
            self.lblNoFilm.setVisible(True)
            self.lblNoFilm.setText("There is no result for this research")

        if Movie.query().count()==0:
            self.lblNoFilm.setVisible(True)
            self.lblNoFilm.setText("No film in database, please add a folder (File - add folder)")
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
        if isinstance(event, ShowFrame) and event.frame == self.__class__.__name__ and event.data is not None:
            self.updateWidgets(event.data)


class ResultRow(QWidget):

    show = pyqtSignal()
    def __init__(self, parent, movie):
        """
            This widget is used as Widget item of a QListWidget
            :param parent: parent of the widget
            :param movie: film information
            :type parent: QWidget
            :type movie: film model
        """
        super(ResultRow,self).__init__(parent)
        self.film = movie
        self.createWidgets(movie)

    def createWidgets(self, movie):
        grid = QGridLayout(self)
        lblImg = QPoster(self, movie.poster)
        dateRelease = ""
        if movie.release is not None:
            dateRelease = str(movie.release)

        #self.importPosterFilm(data.poster)
        if movie.name is not None:
            if movie.genre is not None:
                lblTitle = QLabel(movie.name + " ( " + movie.genre + " )", self)
            else:
                lblTitle = QLabel("Title: " + movie.name, self)
        else:
            lblTitle = QLabel("Title: -", self)
        if movie.actors is not None:
            lblActors = QLabel("Actor(s): " + movie.actors, self)
        else:
            lblActors = QLabel("Actors(s): -",self)
        if movie.directors is not None:
            lblRating = QLabel("IMDb Rating: " + movie.rate, self)
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
    from mawie.gui import start
    start()