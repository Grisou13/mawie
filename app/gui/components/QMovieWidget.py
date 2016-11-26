import sys
from PyQt5.QtWidgets import QWidget, QLabel,QPushButton,QGridLayout,QListWidget
from PyQt5.QtGui import QPixmap,QFont,QImage
from PyQt5.QtCore import QRect,Qt
from urllib import request
from app.gui.components import GuiComponent
from app.models.Movie import Movie

class MovieFrame(QWidget, GuiComponent):
    def __init__(self,parent=None, gui=None):
        super().__init__(parent)
        self.gui = gui
        self.gui.register_listener(self)
        self.initFrame()

    def initFrame(self):
        self.createWidgets()
        self.updateWidgets(Movie.get(7))
        self.show()

    def createWidgets(self):
        grid = QGridLayout()
        fontTitle = QFont('Arial',20)
        fontInfo = QFont('Arial',8)
        imgPix = QPixmap('noPoster.jpg')

        self.lblImg = QLabel(self)
        self.lblImg.setFixedSize(300, 465)
        self.lblImg.setScaledContents(True)

        self.lblTitle = QLabel("*No Title*",self)
        self.lblImg.setPixmap(imgPix)
        self.lblScenarist = QLabel("Writer : -", self)
        self.lblDirector = QLabel("Director: -", self)
        self.lblActors = QLabel("Actor(s): -",self)
        self.lblRuntime = QLabel("Runtime: -",self)
        self.lblRate = QLabel("IMDb Rate: -",self)
        self.lblAwards = QLabel("Awards : -",self)
        self.lblCountry = QLabel("Country : -",self)
        self.lblRelease = QLabel("Release date : -",self)
        self.lblPlot = QLabel("Plot: -",self)
        self.lstFile = QListWidget(self)

        #Set font to labels
        self.lblTitle.setFont(fontTitle)
        self.lblScenarist.setFont(fontInfo)
        self.lblDirector.setFont(fontInfo)
        self.lblActors.setFont(fontInfo)
        self.lblRuntime.setFont(fontInfo)
        self.lblRate.setFont(fontInfo)
        self.lblAwards.setFont(fontInfo)
        self.lblCountry.setFont(fontInfo)
        self.lblRelease.setFont(fontInfo)
        self.lblPlot.setFont(fontInfo)

        self.lblTitle.setWordWrap(True)
        self.lblScenarist.setWordWrap(True)
        self.lblDirector.setWordWrap(True)
        self.lblActors.setWordWrap(True)
        self.lblRuntime.setWordWrap(True)
        self.lblRate.setWordWrap(True)
        self.lblAwards.setWordWrap(True)
        self.lblCountry.setWordWrap(True)
        self.lblRelease.setWordWrap(True)
        self.lblPlot.setWordWrap(True)
        btnLauchnFilm = QPushButton("Launch Film",self)

        grid.addWidget(self.lblImg, 1, 0, 8, 0)

        grid.addWidget(self.lblTitle,0, 0, 1, 2)
        grid.addWidget(self.lblScenarist,1,1)
        grid.addWidget(self.lblDirector,2,1)
        grid.addWidget(self.lblActors,3,1)
        grid.addWidget(self.lblRuntime,4,1)
        grid.addWidget(self.lblRate,5,1)
        grid.addWidget(self.lblAwards,6,1)
        grid.addWidget(self.lblCountry,7,1)
        grid.addWidget(self.lblRelease,8,1)
        grid.addWidget(self.lblPlot,9,0,1,2)
        grid.addWidget(self.lstFile,10,0,1,2)
        grid.addWidget(btnLauchnFilm,11,0,2,2)
        self.setLayout(grid)
    def updateWidgets(self,film):
        if film.poster is not None:
            poster = self.importPosterFilm(film.poster)
        else :
            poster = self.importPosterFilm()
        self.lblImg.setPixmap(poster)
        if film.name is not None:
            self.lblTitle.setText(film.name)
        else:
            self.lblTitle.setText("*no title*")
        if film.writer is not None:
            self.lblScenarist.setText("Scenarist: "+film.writer)
        else:
            self.lblScenarist.setText("Scenarist: -")
        if film.directors is not None:
            self.lblDirector.setText("Directors: "+film.directors)
        else:
            self.lblDirector.setText("Directors: -")
        if film.actors is not None:
            self.lblActors.setText("Actors :"+film.actors)
        else:
            self.lblActors.setText("Actors : -")
        if film.runtime is not None :
            self.lblRuntime.setText("Runtime: " + film.runtime)
        else:
            self.lblRuntime.setText("Runtime: -")
        if film.rate is not None:
            self.lblRate.setText("Rate IMDb: "+ film.rate)
        else:
            self.lblRate.setText("Rate IMDb: -")
        # if film.awards is not None:
        #     self.lblAwards.setText("Awards: "+film.awards)
        # else:
        #     self.lblAwards.setText("Awards: -")
        # if film.Country is not None:
        #     self.lblCountry.setText("Country: "+film.Country)
        # else:
        #     self.lblCountry.setText("Country: -")
        if film.release is not None:
            self.lblRelease.setText("Release: "+str(film.release))
        else:
            self.lblRelease.setText("Release: -")
        if film.desc is not None:
            self.lblPlot.setText("Plot: "+film.desc)
        else:
            self.lblPlot.setText("Plot: -")

        if len(film.files) == 1:
            self.lstFile.hide()
        else:
            for file in film.files:
                self.lstFile.addItem(file.path)
            self.lstFile.show()

    def seeBtnClicked(self):
        pass
    def importPosterFilm(self, path=''):
        image = QImage()
        pixMap = QPixmap("noPoster.jpg")
        if path is '':
            return pixMap
        try:
            html = request.urlopen(path)
            data = html.read()
            flag = False
            image.loadFromData(data)
            pixMap = QPixmap(image)
        except request.URLError:  # in case there isn't the internet or the url gives 404 error or bad url
            print("a problem with the connection or the url has occurred")
        return pixMap

    def handleAction(self, name, data):
        if name == "show-info-film":
            self.updateWidgets(data)
            self.gui.dispatchAction("show-frame",MovieFrame)

    def requestAction(self, name):
        pass
