import os
import sys

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QLabel,QPushButton,QGridLayout,QListWidget
from PyQt5.QtGui import QPixmap,QFont,QImage
from PyQt5.QtCore import QRect,Qt
from urllib import request

from qtpy import QtCore

from app.gui.components import GuiComponent
from app.gui.components.QMoviePlayer import VideoPlayer
from app.models.Movie import Movie

class MovieFrame(QWidget, GuiComponent):
    def __init__(self,parent=None, gui=None):
        super().__init__(parent)
        self.gui = gui
        self.gui.register_listener(self)
        self.initFrame()

    def initFrame(self):
        self.createWidgets()
        #self.updateWidgets(Movie.get(7))
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
        self.lstFile.setMaximumHeight(100)

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

        self.btnLaunchFilm = QPushButton("Watch Film",self)
        self.btnLaunchFilm.setMinimumWidth(300)
        self.btnLaunchFilm.clicked.connect(self.btnSeeClicked)


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
        grid.addWidget(self.btnLaunchFilm,10,0,2,2,QtCore.Qt.AlignCenter)
        self.setLayout(grid)

    def updateWidgets(self,film):
        self.film = film
        if self.film.poster is not None:
            poster = self.importPosterFilm(self.film.poster)
        else :
            poster = self.importPosterFilm()
        self.lblImg.setPixmap(poster)
        if self.film.name is not None:
            self.lblTitle.setText(self.film.name)
        else:
            self.lblTitle.setText("*no title*")
        if self.film.writer is not None:
            self.lblScenarist.setText("Scenarist: "+self.film.writer)
        else:
            self.lblScenarist.setText("Scenarist: -")
        if self.film.directors is not None:
            self.lblDirector.setText("Directors: "+self.film.directors)
        else:
            self.lblDirector.setText("Directors: -")
        if self.film.actors is not None:
            self.lblActors.setText("Actors :"+self.film.actors)
        else:
            self.lblActors.setText("Actors : -")
        if self.film.runtime is not None :
            self.lblRuntime.setText("Runtime: " + self.film.runtime)
        else:
            self.lblRuntime.setText("Runtime: -")
        if self.film.rate is not None:
            self.lblRate.setText("Rate IMDb: "+ self.film.rate)
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
        if self.film.release is not None:
            self.lblRelease.setText("Release: "+str(self.film.release))
        else:
            self.lblRelease.setText("Release: -")
        if self.film.desc is not None:
            self.lblPlot.setText("Plot: "+self.film.desc)
        else:
            self.lblPlot.setText("Plot: -")

        if len(self.film.files) == 1:
            self.lstFile.hide()
            self.btnLaunchFilm.show()
        elif len(self.film.files) >= 1:
            self.lstFile.clear() #we clear the list just to be sure there isn't any items inside the list from another movie
            for file in self.film.files:
                item = QListWidgetItem(self.lstFile)
                itemW = FileWidget(self, file)
                item.setSizeHint(itemW.sizeHint())
                self.lstFile.setItemWidget(item, itemW)
                itemW.btnPlayFile.clicked.connect(lambda ignore, x=file: self.btnPlayFileClicked(x))
            self.lstFile.show()
            self.btnLaunchFilm.hide()


    def btnSeeClicked(self):
        if len(self.film.files) is 1:
            if os.path.isfile(self.film.files[0].path):
               #os.startfile(self.film.files[0].path)
               moviePlayer = VideoPlayer(path = self.film.files[0].path)
               moviePlayer.exec_()
            else:
                self.displayErrorMessage("This file doesn't exit", "This file doesn't exist anymore, "
                                                                    "it has maybe been deleted or moved in an other folder")
    def btnPlayFileClicked(self,file=None):
        if os.path.isfile(file.path):
            #os.startfile(file.path) # display in the default player of the user
            moviePlayer = VideoPlayer(path=file.path)
            moviePlayer.exec_()
        else:
            self.displayErrorMessage("This file doesn't exit", "This file doesn't exist anymore, "
                                                           "it has been deleted or moved in another folder")


    def importPosterFilm(self, path=''):
        image = QImage()
        pixMap = QPixmap(os.path.join(os.path.realpath(__file__),"../../../../",".cache","noPoster.jpg"))
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

    def displayErrorMessage(self,title="-",text="-"):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()


class FileWidget(QWidget):
    def __init__(self,parent=None,file=None):
        super(FileWidget, self).__init__(parent)
        self.createWidget(file)

    def createWidget(self,file):
        grid = QGridLayout()
        fileLabel = QLabel(file.path)
        fileLabel.setFixedWidth(500)
        fileLabel.setWordWrap(True)

        self.btnPlayFile= QPushButton("Play this file")

        grid.addWidget(fileLabel,0,0)
        grid.addWidget(self.btnPlayFile,0,1)
        self.setLayout(grid)
