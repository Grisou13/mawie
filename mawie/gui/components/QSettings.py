import os

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from sqlalchemy import event

from mawie.events.gui import ShowSettings, ShowFrame
from mawie.gui.components import GuiComponent
from mawie.models import db
from mawie.models.File import File
from mawie.models.Movie import Movie

import logging
log = logging.getLogger("mawie")

#TODO:

# First Launch - Create folders and stuff

# Erase database data
# Folder deleting V


class SettingsWidget(GuiComponent):
    """
    Short
    Long
    """
    def __init__(self,parent=None,gui=None):
        """
        Short
        Long
        :param parent:
        :type parent: QWidget
        :param gui:
        """
        super(SettingsWidget,self).__init__(parent)
        self.gui = gui
        self.createWidgets()

    def createWidgets(self):
        grid = QGridLayout()
        font = QFont('',18)
        fontSubTitle = QFont('',12)
        self.settings = QSettings()

        updatorEnable= self.settings.value("updator/updatorEnable")
        frequency = self.settings.value("updator/frequency")
        playerDefault = self.settings.value("infomovie/player-default")




        lblTitle= QLabel("Settings",self)
        lblTitle.setFont(font)
        chkDefaultSystemPlayer = QCheckBox("Only use default video player to play movie",self)
        chkUpdatorEnable = QCheckBox("Enabled updator",self)
        lblFrequency = QLabel("Frequency you want the updator checked your files")
        cboFrequency = QComboBox(self)
        lblDeleteDb = QLabel("Delete the database : it will erase all the movie and associates files in the database",self)
        btnDeleteDb = QPushButton("Erase the database",self)
        lblLstDir = QLabel("List of the directories it will search movies",self)
        lblLstDir.setFont(fontSubTitle)
        self.lstDir = QListWidget(self)

        cboFrequency.addItem("every 30 seconds")
        cboFrequency.addItem("every 3 minutes")
        cboFrequency.addItem("every 10 minutes")
        cboFrequency.addItem("every hour")

        if updatorEnable == 'true':
            chkUpdatorEnable.setChecked(True)
        elif updatorEnable == 'false':
            chkUpdatorEnable.setChecked(False)

        if playerDefault == 'true':
            chkDefaultSystemPlayer.setChecked(True)
        elif playerDefault == 'false':
            chkDefaultSystemPlayer.setChecked(False)

        if frequency == 300:
            cboFrequency.setCurrentIndex(0)
        elif frequency == 1800:
            cboFrequency.setCurrentIndex(1)
        elif frequency == 6000:
            cboFrequency.setCurrentIndex(2)
        elif frequency == 36000:
            cboFrequency.setCurrentIndex(3)


        listDir = File.query(File.base.distinct())
        for dir in listDir :
            directoryPath = dir[0]
            #print(directoryPath)
            item = QListWidgetItem(self.lstDir)
            itemW = DirListItem(self.lstDir, directoryPath)
            item.setSizeHint(itemW.sizeHint())
            self.lstDir.setItemWidget(item, itemW)
            itemW.btnDelDir.clicked.connect(lambda ignore, x=directoryPath, y=item: self.deleteDirClicked(dirPath = x,
                                                                                                          item=y))

        chkDefaultSystemPlayer.stateChanged.connect(self.defaultPlayerChecked)
        chkUpdatorEnable.stateChanged.connect(self.updatorChecked)
        cboFrequency.currentIndexChanged.connect(self.frequencyChanged)
        btnDeleteDb.clicked.connect(self.eraseDbClicked)

        grid.addWidget(lblTitle,0,0,1,2)
        grid.addWidget(chkDefaultSystemPlayer,1,0,1,2)
        grid.addWidget(chkUpdatorEnable,2,0,1,2)
        grid.addWidget(lblFrequency,3,0)
        grid.addWidget(cboFrequency,3,1)
        grid.addWidget(lblDeleteDb,4,0,1,1)
        grid.addWidget(btnDeleteDb,4,1,1,1)
        grid.addWidget(lblLstDir,5,0)
        grid.addWidget(self.lstDir,6,0,1,2)
        self.setLayout(grid)

    def deleteDirClicked(self,dirPath=None, item=None):
        response = QMessageBox.question(self, "Delete folder ?",
                                        "Are you sure you want to delete this folder ? This will delete all metadata"
                                        " of movies that were contained in the folder",
                                        QMessageBox.Yes | QMessageBox.Cancel)
        if response == QMessageBox.Yes:
            listFileInDir = File.query().filter(File.base == dirPath)
            row = self.lstDir.row(item)
            for file in listFileInDir:
                movieId = file.movie_id
                movie = Movie.get(movieId)
                file.delete()
                if movie is not None:
                    if len(movie.files) == 0:
                        movie.delete()
            self.lstDir.takeItem(row)

    def defaultPlayerChecked(self,status):
        if status == 0:
            self.settings.setValue("infomovie/player-default",False)

        else:
            self.settings.setValue("infomovie/player-default",True)

    def updatorChecked(self,status):
        if status == 0:
            self.settings.setValue("updator/updatorEnable",False)
        else:
            self.settings.setValue("updator/updatorEnable",True)

    def eraseDbClicked(self):
        response = QMessageBox.question(self, "Erase database ?", "Are you sure you want to erase all the database ?"
                                                                  " it will delete all the metadata of movies",
                                        QMessageBox.Yes | QMessageBox.Cancel)
        if response == QMessageBox.Yes:
            db.drop_all()  # clear the database you know?
            db.create_all()
            self.lstDir.clear()

    def displayQuestionMessage(self,title="-",text="-",icon=None):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msgBox.exec()

    def frequencyChanged(self,idx):
        if idx == 0:
            self.settings.setValue("updator/frequency",300)
        elif idx == 1:
            self.settings.setValue("updator/frequency", 1800)
        elif idx == 2:
            self.settings.setValue("updator/frequency", 6000)
        elif idx == 3:
            self.settings.setValue("updator/frequency", 36000)

    def handle(self,event):
        super().handle(event)


class DirListItem(QWidget):
    def __init__(self,parent = None,dirPathFile=None):
        super(DirListItem, self).__init__(parent)
        self.dirPath = dirPathFile
        log.info(self.dirPath)
        self.createWidgets()

    def createWidgets(self):
        grid = QGridLayout()
        lblDirPath = QLabel(self.dirPath,self)
        lblDirPath.setMinimumWidth(400)

        self.btnDelDir = QPushButton("Delete this folder",self)
        self.btnDelDir.setMaximumWidth(300)
        grid.addWidget(lblDirPath,0,0)
        grid.addWidget(self.btnDelDir,0,1)
        self.setLayout(grid)