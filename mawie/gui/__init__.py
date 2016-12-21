import logging
import sys
import threading
import time

import qdarkstyle
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QPushButton, QGridLayout, \
    QMainWindow

from mawie.app import App
from mawie.app import start as startApp
from mawie.events import Listener, EventManager
from mawie.events import Quit, Response, Request
from mawie.events.gui import *
from mawie.gui.QMainWindow import MainWindow
from mawie.gui.components.QAdvancedSearchWidget import AdvancedSearch
from mawie.gui.components.QErrorWidget import ErrorWidget
from mawie.gui.components.QExplorerWidget import ExplorerWidget
from mawie.gui.components.QMovieListWidget import MovieListWidget
from mawie.gui.components.QResearchWidget import ResearchWidget
from mawie.gui.components.QSettings import SettingsWidget
from mawie.gui.components.QComponentAreaWidget import ComponentArea

log = logging.getLogger(__name__)
started = False  # flag to tell wether the app is started

_gui_instance = None


class BackgorundProcess(QThread, Listener):
    _lock = threading.Lock()
    request = pyqtSignal("PyQt_PyObject")  # use QT signals to communicate between threads
    response = pyqtSignal("PyQt_PyObject")  # use QT signals to communicate between threads

    def __init__(self):
        super(BackgorundProcess, self).__init__()
        self.app = App()
        self.request.connect(self.app.emit)

    def dispatchInternal(self, event):
        # explicitly add an event to the app, it is normal to not call handle, since the app is supposed to use a queue to handle the events
        self.request.emit(lambda e: self.app.emit(e))


    def run(self):
        self.app.registerListener(self, "front")  # register it with a tag of front
        time.sleep(1.2)
        startApp(self.app)
        log.info("connected app to gui")

    def handle(self, event):
        if isinstance(event, Response) or (
                        isinstance(event, Request) and event.response is not None and isinstance(event.response,
                                                                                                 Response)):
            log.info("IN THREAD SENDING BACK %s", event)
            self.response.emit(event)  # propagate back to foreground
            # event.stopPropagate()



# def singleton(cls):
#     # instance = None
#     def ctor(*args, **kwargs):
#         global instance
#         if not instance:
#             log.info("-------------------")
#             log.info("creating class %s", cls)
#             log.info("%s %s", args, kwargs)
#             log.info("-----------------")
#             instance = cls(*args, **kwargs)
#         return instance
#
#     return ctor
#
#
# class Singleton(type):
#     _instances = {}
#
#     #
#     # def __new__(cls, *arg, **kwargs):
#     #     if cls.__instance is None:
#     #         cls.__instance = object.__new__(cls)
#     #     else:
#     #         log.info("#################")
#     #         log.info("singleton works")
#     #         log.info("#################")
#     #     log.info("gui started = %s", Gui.__instance.started)
#     #     log.info("%s",cls.__instance)
#     #     return cls.__instance
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]


class Gui(EventManager):
    started = False
    main = None  # reference to the main window

    def __init__(self, app=None):
        super().__init__()
        log.info("Gui instance %s [started = %s]", self, self.started)

        if not hasattr(self, "app"):
            self.app = app  # container for the main QtApplication not mawie.app
        if not self.started:
            self.started = True
            self.initUI()

    def initUI(self):
        log.info("#########################################")
        self.registerSettings()
        log.info("STARTING GUI COMPONENTS")

        self.registerListener(self, "self")
        self.backgroundProcessThread = BackgorundProcess()
        self.main = MainWindow(self)

        self.registerListener(self.main)
        # self.main.initWidget()
        # self.errorWidget = ErrorWidget(self.main)
        # self.errorWidget.show()
        self.registerExceptions()
        log.info("GUI ELEMENTS STARTED")
        thread = self.backgroundProcessThread
        thread.response.connect(lambda e: self.emit(e))
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

    def errorHandling(self, ErrorType, ErrorValue, TraceBack):
        """
        Handles any incomming error from either python or Qt
        :param ErrorType:
        :param ErrorValue:
        :param TraceBack:
        :return:
        """
        if not isinstance(TraceBack, str):
            traceback.print_exc()
        else:
            log.warning(TraceBack)
        self.emit(ErrorEvent(ErrorType, ErrorValue, TraceBack))



    def registerExceptions(self):
        if not self.started:
            sys.excepthook = self.errorHandling
            QtCore.qInstallMessageHandler(self.errorHandling)

    def handle(self, event):
        log.info("module name %s", __name__)
        if isinstance(event, ErrorEvent):
            log.warning("Error %s: %s \n\n[%s] \n \n", event.type, event.value, event.traceback)
        else:
            log.info("handling events: %s [timeout = %s]", event, event.timeout)

        # if isinstance(event, Start):
        #     pass
        if isinstance(event, Quit):
            self.backgroundProcessThread.terminate()
            if hasattr(self, "app"):
                self.app.quit()
            else:
                QApplication.instance().quit()
        elif isinstance(event, Request):
            log.info("emitting to background process %s", event)
            self.backgroundProcessThread.request.emit(event)
            # event.stopPropagate() #TODO handle the event a bit better, to look if we don't want to forward the reuqest to compoenents
        elif isinstance(event, Response):
            self.emit(event, "default")
            # event.stopPropagate()


def instance(*args, **kwargs):
    global _gui_instance
    if _gui_instance is None:
        log.info("getting instance of gui")
        _gui_instance = Gui(*args, **kwargs)
    return _gui_instance


def start():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setOrganizationName("CPNV")
    app.setApplicationName("MAWIE")
    gui_ = instance(app)
    # QTimer.singleShot(12*10000,lambda g = ex:ex.emit(Quit())) #after a minute just quit the app, so that debugging is easier
    code = app.exec()
    traceback.print_exc()
    sys.exit(code)


if __name__ == '__main__':
    start()
