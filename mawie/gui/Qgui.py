
import copy
import os
import sys
import threading
import weakref
from PyQt5 import QtGui

from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtCore import QPropertyAnimation

from PyQt5.QtCore import QResource
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt, QRunnable, QThread, QThreadPool, pyqtSignal, QObject

from mawie.app import App
from mawie.events import Eventable, Start, Listener, EventManager
from mawie.events.search import SearchRequest, SearchResponse
from mawie.gui.components import GuiComponent
from mawie.gui.components import QAdvancedSearch
from mawie.gui.components import QExplorer
from mawie.gui.components import QMovieListWidget
from mawie.gui.components.QAdvancedSearch import AdvancedSearch
from mawie.gui.components.QResearchWidget import ResearchFrame
from mawie.gui.components.QStackedWidget import ComponentArea
from mawie.helpers import Singleton
from mawie.gui.components.QError import ErrorWidget
import mawie.gui.resources.images

import qdarkstyle
import traceback
from mawie.events.gui import *

import logging

from mawie.models.Movie import Movie

log = logging.getLogger("mawie")

class NotAComponent(Exception):
    pass


class BackgorundProcess(QObject,Listener):
    send = pyqtSignal("PyQt_PyObject")
    response = pyqtSignal("PyQt_PyObject")
    def dispatchInternal(self,event):
        self.app.addEvent(event)
    def run(self):
        print("starting")
        self.app = App()

        self.app.registerListener(self)
        self.send.connect(self.dispatchInternal)
        self.app.emit(Start())
    def handle(self,event):
        self.response.emit(event)

class MainWindow(QMainWindow, GuiComponent):
    def __init__(self):
        super().__init__()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def initWidget(self):
        bar = self.menuBar()
        menu = bar.addMenu("Menu")

        menuAddFolder = QAction("Add folder", self)
        menuAddFolder.triggered.connect(lambda: self.emit(ShowExplorer()))
        menu.addAction(menuAddFolder)

        menuSettings = QAction("Settings", self)
        menuSettings.triggered.connect(lambda: self.emit(ShowSettings()))
        menu.addAction(menuSettings)

        # menuResearch= menu.addMenu("Research")
        # menuResearch.addAction("Advanced research").triggered.connect(lambda: self.emit(ShowFrame(QAdvancedSearch.__class__.__name__)))
        # menuResearch.addAction("Standard research").triggered.connect(lambda: self.emit(ShowFrame(QMovieListWidget.__class__.__name__)))

        quit = QAction("Quit", self)
        quit.triggered.connect(self.close)
        menu.addAction(quit)

        self.statusBar().showMessage("STATUS BAR")

        mainWidget = QWidget(self) #central placeholder widget
        self.main = mainWidget
        self.setCentralWidget(self.main)

        content = QGridLayout(mainWidget)
        self.componentArea = ComponentArea(mainWidget)

        mainWidget.setMinimumSize(700, 800)
        self.center()

        # # Make the topbar
        recherche = ResearchFrame(mainWidget)
        # ****** DELETE THE FALLOWING LINEs
        #btnAdvancedSearch = QPushButton("Advanced search", self)
        #btnAdvancedSearch.clicked.connect(lambda x: self.emit(ShowFrame(AdvancedSearch.__name__)))

        self.setWindowTitle('Find My movie')
        self.errorWidget = ErrorWidget(self) # doesn't allow to access menu
        self.errorWidget.move(100,100)

        content.addWidget(recherche, 1, 0)
        #content.addWidget(btnAdvancedSearch, 1, 1)
        content.addWidget(self.componentArea, 2, 0)
        mainWidget.setLayout(content)


class Gui(EventManager, metaclass=Singleton):
    #based out of tornado ioloop https://github.com/tornadoweb/tornado/blob/master/tornado/ioloop.py
    def __init__(self):
        super(Gui, self).__init__()
        self.registerListener(self)
        self.initSettings()
    def initSettings(self):
        settings = QSettings()

        firstLaunch = settings.value("firstlaunch")
        updatorEnable = settings.value("updator/updatorEnable")
        frequency = settings.value("updator/frequency")
        playerDefault = settings.value("infomovie/player-default")

        if firstLaunch is None:
            settings.setValue("firstlaunch", True)
        if updatorEnable is None:
            settings.setValue("updator/updatorEnable", True)
        if frequency is None:
            settings.setValue("updator/frequency", 1800)
        if playerDefault is None:
            settings.setValue("infomovie/player-default", True)

    def initUI(self):
        self.main = MainWindow()
        self.errorWidget = ErrorWidget(self.main)
        self.main.initWidget()
        self.main.show()

    def errorHandling(self,ErrorType, ErrorValue, TraceBack):
        if not isinstance(TraceBack,str):
            traceback.print_exc()
        else:
            print(TraceBack)
        #self.emit(ErrorEvent(ErrorType,ErrorValue,TraceBack))
        self.addError("Error [" + str(ErrorType) + "] : " + str(ErrorValue))

    def addError(self,text):
        self.errorWidget.updateText(text)
        self.errorWidget.display()

    def registerExceptions(self):
        sys.excepthook = self.errorHandling
        QtCore.qInstallMessageHandler(self.errorHandling)

    def handle(self, event):
        print(event)
        #
        # Debugging to remove
        # TODO remove the following
        #
        if isinstance(event,SearchRequest):
            self.emit(SearchResponse(Movie.query(Movie.name.distinct).all()))

        if isinstance(event,Start):
            log.info("Starting app")
            self.initUI()
            self.registerExceptions()
            self.backgroundApp = BackgorundProcess()
            thread = QThread()
            self.backgroundApp.moveToThread(thread)
            self.backgroundApp.response.connect(self.emit)
            thread.run()
            #log.debug("%s background thread")
            self.backgroundProcessThread = thread

        elif not isinstance(event,ShowFrame):
            self.sendToBackground(event)

    def sendToBackground(self,event):
        self.backgroundApp.send.emit(event)

def start():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setOrganizationName("CPNV")
    app.setApplicationName("MAWIE")

    ex = Gui()
    ex.emit(Start())
    code = 0
    try:
        # raise Exception("Test exception")
        code = app.exec()
    except:
        ex.initUI()
    traceback.print_exc()
    sys.exit(code)


if __name__ == '__main__':
    start()
