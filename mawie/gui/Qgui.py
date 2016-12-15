
import copy
import os
import sys
import threading
import weakref

import time
from PyQt5 import QtGui

from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtCore import QPropertyAnimation

from PyQt5.QtCore import QResource
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt, QRunnable, QThread, QThreadPool, pyqtSignal, QObject

from mawie.app import App, start as startApp
from mawie.events import Eventable, Start, Listener, EventManager, Quit, Response, Request
from mawie.events.app import MoveToForeground
from mawie.events.search import SearchRequest
from mawie.gui.components import GuiComponent
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


class BackgorundProcess(QThread):
    _lock = threading.Lock()
    request = pyqtSignal("PyQt_PyObject") #use QT signals to communicate between threads
    response = pyqtSignal("PyQt_PyObject") #use QT signals to communicate between threads
    def __init__(self):
        super(BackgorundProcess,self).__init__()
        self.app = App()
        self.request.connect(self.app.addEvent)

    def dispatchInternal(self,event):
        with self._lock:
            self.request.emit(lambda e: self.app.addEvent(e))#explicitly add an event to the app, it is normal to not call handle, sicne the app is supposed to use a queue to handle the events

    def run(self):

        class Local(Listener):
            """
                small inner class, so that the Background process doesnt become a listener.
                It would be too much overhead, and not a good task separation
            """
            def __init__(self, process):
                super().__init__(None)
                self.process = process
            def handle(self, event):
                if isinstance(event, Response) or (isinstance(event,Request) and event.response is not None and isinstance(event.response, Response)):
                    log.info("sending back response from background %s",event)
                    self.process.response.emit(event) #propagate back to foreground
                    event.stopPropagate()
        listener = Local(self)
        self.app.registerListener(listener,"front") #register it with something extra data
        time.sleep(1.2)
        startApp(self.app)
        log.info("connected app to gui")
        #QTimer.singleShot(1000,lambda : self.app.emit(Start())) #start the background process in a second



class MainWindow(QMainWindow):
    def closeEvent(self, *args, **kwargs):
        super(QMainWindow,self).closeEvent(*args,**kwargs)
        Gui().emit(Quit())
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def initWidget(self):
        self.statusBar().showMessage("hi")

        mainWidget = QWidget(self) #central placeholder widget
        self.main = mainWidget
        self.setCentralWidget(self.main)

        content = QGridLayout(mainWidget)
        self.componentArea = ComponentArea(mainWidget)

        mainWidget.setMinimumSize(700, 800)
        self.center()
        # Make the topbar
        recherche = ResearchFrame(mainWidget)
        btnAdvancedSearch = QPushButton("Advanced search", self)
        btnAdvancedSearch.clicked.connect(lambda x: Gui().emit(ShowFrame(AdvancedSearch.__name__)))
        self.setWindowTitle('Find My movie')
        self.errorWidget = ErrorWidget(self)
        content.addWidget(self.componentArea, 2, 0)
        content.addWidget(recherche, 1, 0)
        content.addWidget(btnAdvancedSearch, 1, 1)
        mainWidget.setLayout(content)

class Gui(EventManager, metaclass=Singleton):
    #based out of tornado ioloop https://github.com/tornadoweb/tornado/blob/master/tornado/ioloop.py
    def __init__(self, app = None):
        super(Gui, self).__init__()
        if not hasattr(self,"app"):
            self.app = app #container for the main QtApplication
        self.registerListener(self,"self")
        self.backgroundProcessThread = BackgorundProcess()
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
            log.warning(TraceBack)

        self.emit(ErrorEvent(ErrorType,ErrorValue,TraceBack))
        self.addError("Error [" + str(ErrorType) + "] : " + str(ErrorValue))

    def addError(self,text):
        self.errorWidget.updateText(text)
        self.errorWidget.display()

    def registerExceptions(self):
        sys.excepthook = self.errorHandling
        QtCore.qInstallMessageHandler(self.errorHandling)

    def handle(self, event):
        if isinstance(event, ErrorEvent):
            log.warning("Error %s: %s [%s]",event.type,event.value,traceback.print_tb(event.traceback))
            log.info(traceback.print_exc())
        else:
            log.info("handling events: %s [%s]",event,event.data)

        if isinstance(event,Start):
            log.info("starting everything up")
            self.initUI()
            self.registerExceptions()
            #self.backgroundApp = BackgorundProcess()
            thread = BackgorundProcess()
            thread.started.connect(lambda : log.info("background process started"))
            thread.finished.connect(lambda : log.info("background process stopped"))
            #self.backgroundApp.moveToThread(thread)
            thread.response.connect(self.emit)

            #thread.run()
            log.debug("%s background thread: %s",thread,thread.isRunning())
            self.backgroundProcessThread = thread
            thread.start()
        elif isinstance(event,Quit):
            self.backgroundProcessThread.terminate()
            self.app.quit()
        elif isinstance(event,Request):
            log.info("emitting to background process %s",event)
            self.backgroundProcessThread.request.emit(event)
            event.stopPropagate() #TODO handle the event a bit better, to look if we don't want to forward the reuqest to compoenents

def start():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setOrganizationName("CPNV")
    app.setApplicationName("MAWIE")
    ex = Gui(app)
    ex.initUI()
    time.sleep(1)
    ex.emit(Start())
    time.sleep(2)
    ex.emit(SearchRequest("the"))
    #QTimer.singleShot(12*10000,lambda g = ex:ex.emit(Quit())) #after a minute just quit the app, so that debugging is easier
    code = app.exec()
    traceback.print_exc()
    sys.exit(code)
if __name__ == '__main__':
    start()
