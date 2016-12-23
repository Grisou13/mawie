import sys
import os
from contextlib import suppress
from urllib.parse import urlparse

from PyQt5.QtCore import QRect, QRunnable, QThreadPool, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.uic.properties import QtGui
from PyQt5.QtWidgets import QFileDialog
import qtawesome as qta
from six import unichr

from mawie import helpers
from mawie.events.gui import ShowExplorer, ShowFrame, HideSearch
from mawie.gui.components import GuiComponent
from mawie.events import *
from mawie.events.explorer import *
import time
import sys
import traceback
import copy


class FileParsedListWidget(QListWidget):
    def __init__(self,parent = None):
        super(FileParsedListWidget,self).__init__(parent)
        self.files = {} #keeps track of {filename : widget item}

    def addItem(self,file_):
        if file_ in self.files:
            return
        log.info("adding PARSED item %s", file_)
        item = QListWidgetItem(self)
        self.files[file_] = item
        itemW = FileParsedWidget(self, file_)
        item.setSizeHint(itemW.sizeHint())
        self.setItemWidget(item, itemW)

    def removeItem(self,file_):
        log.info("removing item %s form non parsed", file_)
        with suppress(Exception):
            item = self.takeItem(self.row(self.files[file_]))


class FileNotParsedListWidget(QListWidget):
    def __init__(self,parent):
        super(FileNotParsedListWidget,self).__init__(parent)
        self.files = {}#keeps track of {filename : widget item}

    def removeItem(self,file_):
        log.info("removing item %s form non parsed", file_)
        with suppress(Exception):
            item = self.takeItem(self.row(self.files[file_]))

    def addItem(self,file_):
        if file_ in self.files:
            return
        log.info("adding NON PARSED item %s", file_)
        item = QListWidgetItem(self)
        itemW = FileNotParsedWidget(self, file_)
        self.files[file_] = item
        item.setSizeHint(itemW.sizeHint())
        self.setItemWidget(item, itemW)


class ExplorerWidget(GuiComponent):
    """
    This widget contains everything to make requests to the explorer.
    This widget still needs some improvement.
    As of right now this component doesn't allow the user to force a file with a certain imdb url.

    """
    def __init__(self, parent):
        super(ExplorerWidget,self).__init__(parent)
        self.dirPath = None
        self.initWidget()
        self.show()

    def onShowFrame(self):
        self.emit(HideSearch())

    def initWidget(self):
        content = QGridLayout()

        self.inputPath = QLineEdit(self)
        self.inputPath.setPlaceholderText("No folder selected")
        self.inputPath.setReadOnly(True)

        self.btnOpenDir = QPushButton("Select a directory to scan")
        self.btnScan = QPushButton("Scan directory")


        self.lblLstParseFile = QLabel("list of parsed files")
        #self.lstFileParse = QListWidget(self)
        self.lstFileParse = FileParsedListWidget(self)
        self.lblLstNotParseFile = QLabel("list of non parsable files")
        self.lstFileNotParse = FileNotParsedListWidget(self)
        #self.lstFileNotParse = QListWidget(self)
        self.lstFileParse.setMinimumSize(660,200)
        self.lstFileNotParse.setMinimumSize(660,200)

        content.addWidget(self.inputPath, 0,0)
        content.addWidget(self.btnOpenDir,0,1)
        content.addWidget(self.lblLstNotParseFile,1,0)
        content.addWidget(self.lstFileNotParse,2,0,1,3)
        content.addWidget(self.lblLstParseFile,3,0)
        content.addWidget(self.lstFileParse,4,0,1,3)
        self.setLayout(content)
        self.btnOpenDir.clicked.connect(self.chooseDir)

    def scanDir(self):
        if  self.dirPath is not None:
            if os.path.isdir(self.dirPath):
                self.emit(ExplorerParsingRequest(self.dirPath))
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("The directory you selected doesn't exist. Please reselect a new one")
            msgBox.setWindowTitle("No folder selected")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    def chooseDir(self):
        self.dirPath = QFileDialog.getExistingDirectory(self, 'Open file', helpers.BASE_PATH, QFileDialog.ShowDirsOnly)
        self.inputPath.setText(self.dirPath)
        self.scanDir()

    def handle(self,event):
        super().handle(event)
        if isinstance(event, ShowExplorer):
            self.emit(ShowFrame(self))
        elif issubclass(event.__class__,MovieNotParsed):
            self.lstFileNotParse.addItem(event.file)
        elif issubclass(event.__class__,MovieParsed):
            self.lstFileNotParse.removeItem(event.file)
            self.lstFileParse.addItem(event.file)


class FileParsedWidget(QWidget):
    def __init__(self, parent, file_=None):
        super().__init__(parent)
        self.file = file_
        self.createWidgets()

    def createWidgets(self):
        content = QGridLayout()
        lblFile = QLabel(self.file, self)
        label = QLabel(unichr(0xf00c))
        label.setFont(qta.font('fa', 16))
        label.setStyleSheet("QLabel {color : green}")

        lblFile.setFixedWidth(550)
        lblFile.setWordWrap(True)

        content.addWidget(lblFile, 0, 0)
        content.addWidget(label, 0, 1)
        self.setLayout(content)

class FileNotParsedWidget(QWidget):
    def __init__(self,parent,file_=None):
        super().__init__(parent)
        self.file = file_
        self.opened = False
        self.createWidgets()

    def createWidgets(self):
        grid = QGridLayout()
        lblFile = QLabel(self.file,self)
        #faIconCheck = qta.icon("fa.external-link",color="white")
        #self.btnGiveImdbUrl = QPushButton(faIconCheck,"Give IMDb URL",self)
        #self.btnGiveImdbUrl.clicked.connect(self.parseByExplorer)
        #lblFile.setFixedWidth(400)
        lblFile.setWordWrap(True)

        grid.addWidget(lblFile,0,1)
        #grid.addWidget(self.btnGiveImdbUrl,0,2)
        self.setLayout(grid)
    def parseByExplorer(self):
        """
        This function will create a popup asking the user for the imdb url or title of the movie.
        After it will just emit a ExplorerParsingRequest.
        TODO: As of right now the explorer will respond.
              but the commponent can't communicate with the explorer.
        """
        self.opened = True
        idMovie = None
        url = None
        urlPath = None
        itemAdd= None

        url, ok = QInputDialog.getText(self,'Copy IMDb URL or Movie title', 'Please copy the URL of the web page IMDb of the movie:')
        if url is not None and url != "":
            urlParsed = urlparse(url)
            urlPath = urlParsed.path
            idMovie = urlPath.split("title/")[1][:-1]

            if idMovie is not None or idMovie is not "":
                self.parent.emit(GoogleItSearchRequest({"file":self.file,"url":url}))
                # TODO: add file to a database
            else:
                self.parent.emit(GoogleItSearchRequest({"file":self.file,"title":url}))
