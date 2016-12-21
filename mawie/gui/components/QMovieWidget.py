import os
import subprocess
import platform

import time

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget, QLabel,QPushButton,QGridLayout,QListWidget
from PyQt5.QtGui import QPixmap,QFont,QImage
from PyQt5.QtCore import QRect,Qt
from urllib import request

from PyQt5 import QtCore

from mawie.events.gui import ShowFrame, ShowMovieInfo, ShowMovieList
from mawie.events.search import SearchRequest

from mawie.gui.components import GuiComponent


from mawie.gui.components.QPoster import QPoster
from mawie.gui.components.QMoviePlayer import MoviePlayer
from mawie.models.File import File
from mawie.models.Movie import Movie
import qtawesome as qta
import logging
log = logging.getLogger("mawie")

class MovieWidget(GuiComponent):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.settings = QSettings()
        self.initFrame()

    def initFrame(self):
        self.createWidgets()
        self.show()

    def createWidgets(self):
        grid = QGridLayout()
        headerLayout = QHBoxLayout()
        fontTitle = QFont('Arial',20)
        fontInfo = QFont('Arial',8)
        goBackIcon = qta.icon('fa.chevron-left',
                                 active='fa.chevron-left',
                                 color='white',
                                 color_active='white')

        self.lblImg = QPoster(self) #QLabel(self)
        self.lblImg.setMaximumSize(300, 465)
        self.lblImg.setScaledContents(True)

        self.btnGoBack = QPushButton(goBackIcon,"Return",self)
        self.btnGoBack.setMaximumWidth(100)
        self.btnGoBack.clicked.connect(self.btnGoBackClicked)
        self.lblTitle = QLabel("<b>*No Title*</b>",self)
        headerLayout.addWidget(self.btnGoBack)
        headerLayout.addWidget(self.lblTitle)


        #self.lblImg.setPixmap(imgPix)
        self.lblScenarist = QLabel("<b>Writer : -</b>", self)
        self.lblDirector = QLabel("<b>Director: -</b>", self)
        self.lblActors = QLabel("<b>Actor(s): -</b>",self)
        self.lblRuntime = QLabel("<b>Runtime: -</b>",self)
        self.lblRate = QLabel("<b>IMDb Rate: -</b>",self)

        self.lblRelease = QLabel("<b>Release date : -</b>",self)
        self.lblPlot = QLabel("<b>Plot: -</b>",self)

        self.lstFile = QListWidget(self)
        self.lstFile.setMaximumHeight(100)

        #Set font to labels
        self.lblTitle.setFont(fontTitle)
        self.lblScenarist.setFont(fontInfo)
        self.lblDirector.setFont(fontInfo)
        self.lblActors.setFont(fontInfo)
        self.lblRuntime.setFont(fontInfo)
        self.lblRate.setFont(fontInfo)

        self.lblRelease.setFont(fontInfo)
        self.lblPlot.setFont(fontInfo)

        self.lblTitle.setWordWrap(True)
        self.lblScenarist.setWordWrap(True)
        self.lblDirector.setWordWrap(True)
        self.lblActors.setWordWrap(True)
        self.lblRuntime.setWordWrap(True)
        self.lblRate.setWordWrap(True)

        self.lblRelease.setWordWrap(True)
        self.lblPlot.setWordWrap(True)

        self.btnLaunchFilm = QPushButton("Play Film",self)
        self.btnLaunchFilm.setMinimumWidth(200)
        self.btnLaunchFilm.clicked.connect(lambda : self.btnPlayFileClicked(file=None))

        self.btnShowInDir = QPushButton("Show in Explorer")
        self.btnShowInDir.setMinimumWidth(200)
        self.btnShowInDir.clicked.connect(lambda: self.btnShowInDirClicked(file=None))

        self.btnDeleteFile = QPushButton("Delete File from Database")
        self.btnDeleteFile.setMinimumWidth(200)
        self.btnDeleteFile.clicked.connect(lambda : self.btnDeleteFileClicked(file=None,item=None))

        #this BoxLayout is used to put the button launch, show in explorer and delete File one the same line
        btnBoxlayout = QHBoxLayout()
        btnBoxlayout.addWidget(self.btnLaunchFilm)
        btnBoxlayout.addWidget(self.btnShowInDir)
        btnBoxlayout.addWidget(self.btnDeleteFile)

        grid.addLayout(headerLayout, 0, 0, 1, 2)
        grid.addWidget(self.lblImg, 1, 0, 6, 2)
        grid.addWidget(self.lblScenarist,1,1,1,1)
        grid.addWidget(self.lblDirector,2,1)
        grid.addWidget(self.lblActors,3,1)
        grid.addWidget(self.lblRuntime,4,1)
        grid.addWidget(self.lblRate,5,1)
        grid.addWidget(self.lblRelease,6,1)
        grid.addWidget(self.lblPlot,7,0,1,2)
        grid.addWidget(self.lstFile,9,0,1,2)
        grid.addLayout(btnBoxlayout,9,0,1,2)
        self.setLayout(grid)

    def updateWidgets(self,film):
        self.film = film
        self.lblImg.updateUrl(self.film.poster)
        #self.lblImg.setPixmap(poster)
        if self.film.name is not None:
            self.lblTitle.setText(self.film.name)
        else:
            self.lblTitle.setText("<b>*no title*")
        if self.film.writer is not None:
            self.lblScenarist.setText("<b>Scenarist: </b>"+self.film.writer)
        else:
            self.lblScenarist.setText("<b>Scenarist: </b>-")
        if self.film.directors is not None:
            self.lblDirector.setText("<b>Directors: </b>"+self.film.directors)
        else:
            self.lblDirector.setText("<b>Directors: </b>-")
        if self.film.actors is not None:
            self.lblActors.setText("<b>Actors :</b>"+self.film.actors)
        else:
            self.lblActors.setText("<b>Actors : </b>-")
        if self.film.runtime is not None :
            self.lblRuntime.setText("<b>Runtime: </b>" + self.film.runtime)
        else:
            self.lblRuntime.setText("<b>Runtime: </b>-")
        if self.film.rate is not None:
            self.lblRate.setText("<b>Rate IMDb: </b>"+ self.film.rate)
        else:
            self.lblRate.setText("<b>Rate IMDb: -</b>")

        if self.film.release is not None:
            self.lblRelease.setText("<b>Release: </b>"+str(self.film.release))
        else:
            self.lblRelease.setText("<b>Release: </b>-")
        if self.film.desc is not None:
            self.lblPlot.setText("Plot: "+self.film.desc)
        else:
            self.lblPlot.setText("Plot: -")

        if len(self.film.files) == 1:
            self.lstFile.hide()
            self.btnLaunchFilm.show()
            self.btnShowInDir.show()
            self.btnDeleteFile.show()
        elif len(self.film.files) >= 1:
            self.lstFile.clear() #we clear the list just to be sure there isn't any items inside the list from another movie
            for file in self.film.files:
                item = QListWidgetItem(self.lstFile)
                itemW = FileWidget(self, file)
                item.setSizeHint(itemW.sizeHint())
                self.lstFile.setItemWidget(item, itemW)
                itemW.btnPlayFile.clicked.connect(lambda ignore, x=file: self.btnPlayFileClicked(x))
                itemW.btnShowInDir.clicked.connect(lambda ignore, x=file: self.btnShowInDirClicked(x))
                itemW.btnDelete.clicked.connect(lambda ignore , x=file, y=item: self.btnDeleteFileClicked(file=x,item=y))
            self.lstFile.show()
            self.btnLaunchFilm.hide()
            self.btnShowInDir.hide()
            self.btnDeleteFile.hide()
        elif len(self.film.files)==0:
            self.lstFile.hide()
            self.btnShowInDir.hide()
            self.btnDeleteFile.hide()
            self.btnLaunchFilm.hide()
    def btnGoBackClicked(self):
        self.gui.emit(ShowFrame('MovieListWidget'))

    def btnShowInDirClicked(self, file=None):
        path = None
        if file is not None and file.path is not None :
           path = file.path
        elif file is None and len(self.film.files) == 1 and self.film.files[0].path is not None :
            path = self.film.files[0].path
        if path is not None:
            if os.name.lower() == "nt":  # because windows
                path = path.replace("/", "\\")
            if os.path.isfile(path):
                #TODO look for MAC AND LINUX DE MERDE
                subprocess.Popen(r'explorer /select,"{}"'.format(path))
            else:
                self.displayErrorMessage("This file doesn't exist", "This file doesn't exist anymore, "
                                                                    "it has been deleted or moved in another folder")


    def btnPlayFileClicked(self, file=None):
        defaultPlayer = self.settings.value("infomovie/player-default")
        path = None
        if file is not None and file.path is not None:
             path = file.path
        elif file is None and len(self.film.files) == 1 and self.film.files[0].path is not None :
            path = self.film.files[0].path


        if path is not None:
            if os.path.isfile(path):
                if defaultPlayer == 'false':
                        moviePlayer = MoviePlayer(path=path)
                        moviePlayer.exec_()
                else:
                    if platform.system() == "Windows":
                        os.startfile(path)
                    elif platform.system() == "Darwin":
                        subprocess.Popen(["open", path])
                    else:
                        subprocess.Popen(["xdg-open", path])
            else:
                self.displayErrorMessage("This file doesn't exist", "This file doesn't exist anymore, "
                                                                    "it has maybe been deleted or moved in an other folder")

    def btnDeleteFileClicked(self, file=None,item=None):
        fileDel = None
        if file is None:
            fileDel = self.film.files[0]
        else:
            fileDel = file
        if item is not None:
            response = QMessageBox.question(self, "Delete file",
                                            "Delete the file from database ? it will not delete the file from your computer",
                                            QMessageBox.Yes  | QMessageBox.Cancel)
            if response == QMessageBox.Yes:
                row = self.lstFile.row(item)
                self.lstFile.takeItem(row)
                if self.lstFile.count() is 1:
                    self.lstFile.hide()
                    self.btnLaunchFilm.show()
                    self.btnDeleteFile.show()
                    self.btnShowInDir.show()
                fileDel.delete()
        else:
            response = QMessageBox.question(self, "Delete the last file of the movie",
                                            "Delete the file and the <b>movie</b> from database ? it will not delete the movie from your computer",
                                            QMessageBox.Yes | QMessageBox.Cancel)
            if response == QMessageBox.Yes:
                fileDel.delete()
                self.film.delete()
                self.emit(SearchRequest(""))
                self.emit(ShowMovieList())



    def importPosterFilm(self, path=''):
        image = QImage()
        pixMap = QPixmap(os.path.join(os.path.realpath(__file__),"../../../../",".cache","noPoster.jpg"))
        if path is '':
            return pixMap
        try:
            html = request.urlopen(path)
            data = html.read()
            image.loadFromData(data)
            pixMap = QPixmap(image)
        except request.URLError:  # in case there isn't the internet or the url gives 404 error or bad url
            print("a problem with the connection or the url has occurred")
        return pixMap

    def handle(self,event):
        super().handle(event)
        if isinstance(event, ShowFrame) and event.frame == self.__class__.__name__:
            self.updateWidgets(event.data)
        #if isinstance(event, ShowFrame) and event.data is not None:
            #log.info("MOVIE INFO-- %s",event.data)
            #self.emit(ShowFrame(self))
            #self.updateWidgets(event.data)

    def displayErrorMessage(self,title="-",text="-"):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
#
# if __name__ == '__main__':
#     from mawie.gui.Qgui import Gui
#     Gui.start()

class FileWidget(QWidget):
    def __init__(self,parent=None,file=None):
        super(FileWidget, self).__init__(parent)
        self.createWidget(file)

    def createWidget(self,file):
        grid = QGridLayout()
        fileLabel = QLabel(file.path)
        fileLabel.setWordWrap(True)

        self.btnPlayFile= QPushButton("Play this file")
        self.btnShowInDir= QPushButton("Show in explorer")
        self.btnDelete = QPushButton("Delete file from database")

        grid.addWidget(fileLabel,0,0,1,3)
        grid.addWidget(self.btnPlayFile,1,0)
        grid.addWidget(self.btnShowInDir,1,1)
        grid.addWidget(self.btnDelete,1,2)
        self.setLayout(grid)

if __name__ == '__main__':
    from mawie.gui.Qgui import start
    start()