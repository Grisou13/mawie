import logging
import sys
import threading
import time

import qdarkstyle
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QPushButton, QGridLayout, \
    QMainWindow

from mawie.app import App, start as startApp
from mawie.events import Start, Listener, EventManager, Quit, Response, Request
from mawie.events.gui import *
from mawie.gui.components.QError import ErrorWidget


log = logging.getLogger(__name__)
started = False  # flag to tell wether the app is started


class NotAComponent(Exception):
    pass


class BackgorundProcess(QThread, Listener):
    _lock = threading.Lock()
    request = pyqtSignal("PyQt_PyObject")  # use QT signals to communicate between threads
    response = pyqtSignal("PyQt_PyObject")  # use QT signals to communicate between threads

    def __init__(self):
        super(BackgorundProcess, self).__init__()
        self.app = App()
        self.request.connect(self.app.emit)

    def dispatchInternal(self, event):
        # with self._lock:
        self.request.emit(lambda e: self.app.emit(e))
        # explicitly add an event to the app, it is normal to not call handle, sicne the app is supposed to use a queue to handle the events

    def run(self):
        class Local(Listener):
            """
                small inner class, so that the Background process doesnt become a listener.
                It would be too much overhead, and not a good task separation
            """

            def __init__(self, process):
                super().__init__(None)
                self.process = process

        # listener = Local(self)
        self.app.registerListener(self, "front")  # register it with something extra data
        time.sleep(1.2)
        startApp(self.app)
        log.info("connected app to gui")
        # QTimer.singleShot(1000,lambda : self.app.emit(Start())) #start the background process in a second

    def handle(self, event):
        if isinstance(event, Response) or (
                        isinstance(event, Request) and event.response is not None and isinstance(event.response,
                                                                                                 Response)):
            log.info("IN THREAD SENDING BACK %s", event)
            self.response.emit(event)  # propagate back to foreground
            event.stopPropagate()


class MainWindow(QMainWindow, Listener):
    """
    Main window class, contains all the widgets

    starts widget automatically, and shows them
    """
    main = None  # reference to the main widget

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Find My movie')
        self.initWidget()
        self.center()
        self.main.show()
        self.show()

    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)
        Gui().emit(Quit())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initWidget(self):
        from mawie.gui.components.QResearchWidget import ResearchFrame
        from mawie.gui.components.QStackedWidget import ComponentArea
        # self.statusBar().showMessage("hi")
        mainWidget = QWidget(self)  # central placeholder widget
        self.setCentralWidget(mainWidget)
        content = QGridLayout(mainWidget)
        self.componentArea = ComponentArea(mainWidget)
        mainWidget.setMinimumSize(700, 800)
        # Make the topbar
        recherche = ResearchFrame(mainWidget)
        btnAdvancedSearch = QPushButton("Advanced search", self)
        btnAdvancedSearch.clicked.connect(lambda x: Gui().emit(ShowAdvancedSearchFrame()))
        self.errorWidget = ErrorWidget(self)
        content.addWidget(self.componentArea, 2, 0)
        content.addWidget(recherche, 1, 0)
        content.addWidget(btnAdvancedSearch, 1, 1)
        mainWidget.setLayout(content)
        self.main = mainWidget
    def handle(self, event):
        if isinstance(event, Start):
            self.initWidget()
        elif isinstance(event,ErrorEvent):
            self.statusBar().showMessage("ERROR [{}] : {}".format(event.type, event.value))
        elif not isinstance(event, Quit):
            self.componentArea.emit(event)

def singleton(cls):
    instance = None
    def ctor(*args, **kwargs):
        nonlocal instance
        if not instance:
            log.info("%s %s",args,kwargs)
            instance = cls(*args, **kwargs)
        return instance
    return ctor

@singleton
class Gui(EventManager):
    started = False
    # __instance = None
    main = None  # reference to the main window
    #
    # def __new__(cls, *arg, **kwargs):
    #     if cls.__instance is None:
    #         cls.__instance = object.__new__(cls)
    #     else:
    #         log.info("#################")
    #         log.info("singleton works")
    #         log.info("#################")
    #     log.info("gui started = %s", Gui.__instance.started)
    #     log.info("%s",cls.__instance)
    #     return cls.__instance

    def __init__(self, app=None):
        super().__init__()
        #self = Gui.__instance
        log.info("Gui instance %s [started = %s]", self, self.started)

        if not hasattr(self, "app"):
            self.app = app  # container for the main QtApplication
        if not self.started:
            self.initUI()
            self.started = True

    def initUI(self):
        if self.started:
            return
        log.info("#########################################")
        self.registerSettings()
        log.info("STARTING GUI COMPONENTS")

        self.registerListener(self, "self")
        self.backgroundProcessThread = BackgorundProcess()
        self.main = MainWindow()

        self.registerListener(self.main, "main")
        # self.main.initWidget()
        self.errorWidget = ErrorWidget(self.main)
        self.errorWidget.show()
        self.registerExceptions()
        log.info("GUI ELEMENTS STARTED")
        thread = self.backgroundProcessThread
        thread.response.connect(lambda e: Gui().emit(e))
        thread.started.connect(lambda: log.info("background process started"))
        thread.finished.connect(lambda: log.info("background process stopped"))
        log.debug("%s background thread: %s", thread, thread.isRunning())
        thread.start()
        log.info("BACKGROUND THREAD STARTED")
        # self.emit(Start())
        # QTimer.singleShot(3000, lambda: self.emit(SearchRequest("the")))

    def registerSettings(self):
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

    # def initUI(self):
    #     if not started:
    #         self.main.show()
    #         self.emit(Start())
    def errorHandling(self, ErrorType, ErrorValue, TraceBack):
        if not isinstance(TraceBack, str):
            traceback.print_exc()
        else:
            log.warning(TraceBack)

        self.emit(ErrorEvent(ErrorType, ErrorValue, TraceBack))
        self.addError("Error [" + str(ErrorType) + "] : " + str(ErrorValue))

    def addError(self, text):
        self.errorWidget.updateText(text)
        self.errorWidget.display()

    def registerExceptions(self):
        if not started:
            sys.excepthook = self.errorHandling
            QtCore.qInstallMessageHandler(self.errorHandling)

    def handle(self, event):
        log.info("module name %s", __name__)
        if isinstance(event, ErrorEvent):
            log.warning("Error %s: %s \n\n[%s] \n \n", event.type, event.value, event.traceback)
        else:
            log.info("handling events: %s [timeout = %s]", event, event.timeout)

        if isinstance(event, Start):
            pass

        if isinstance(event, Quit):
            self.backgroundProcessThread.terminate()
            self.app.quit()
        elif isinstance(event, Request):
            log.info("emitting to background process %s", event)
            self.backgroundProcessThread.request.emit(event)
            # event.stopPropagate() #TODO handle the event a bit better, to look if we don't want to forward the reuqest to compoenents
        elif isinstance(event, Response):
            log.info("#########################")
            log.info("JAJAJAJAJAJA")
            log.info(event.data)
            log.info(event.request)
            self.emit(event, "main")
            event.stopPropagate()
            log.info("#########################")


def start():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setOrganizationName("CPNV")
    app.setApplicationName("MAWIE")
    gui_ = Gui(app)
    # QTimer.singleShot(12*10000,lambda g = ex:ex.emit(Quit())) #after a minute just quit the app, so that debugging is easier
    code = app.exec()
    traceback.print_exc()
    sys.exit(code)


if __name__ == '__main__':
    start()
