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
from mawie.gui.components.QAdvancedSearchWidget import AdvancedSearch
from mawie.gui.components.QErrorWidget import ErrorWidget
from mawie.gui.components.QExplorerWidget import ExplorerWidget
from mawie.gui.components.QMovieListWidget import MovieListWidget
from mawie.gui.components.QResearchWidget import ResearchWidget
from mawie.gui.components.QSettings import SettingsWidget
from mawie.gui.components.QComponentAreaWidget import ComponentArea


class MainWindow(QMainWindow, Listener):
    """
    Main window class, contains all the widgets

    starts widget automatically, and shows them
    """
    main = None  # reference to the main widget

    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.emit = self.gui.emit
        self.setWindowTitle('Find My movie')
        self.initMenu()
        self.initWidget()
        self.center()
        self.show()
        self.main.show()

    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)
        self.gui.emit(Quit())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def registerWidget(self, widget):
        widget.gui = self.gui
        widget.emit = lambda e: self.gui.emit(e)
        if not hasattr(widget,
                       "handle"):  # we define a dumy handle event if the Component doesn't have one, so that the app doesn't freeze
            def dummyHandle(self, event):
                pass

            widget.handle = dummyHandle
        self.gui.registerListener(widget)
        return widget

    def initMenu(self):
        bar = self.menuBar()
        menu = bar.addMenu("&File")
        menuAddFolder = QAction("Add folder", self)
        menuAddFolder.triggered.connect(lambda: self.gui.emit(ShowFrame(ExplorerWidget.__name__)))
        menu.addAction(menuAddFolder)

        quit = QAction("Quit", self)
        quit.triggered.connect(self.close)
        menu.addAction(quit)

        menuSettings = bar.addAction("Settings")
        menuSettings.triggered.connect(lambda: self.emit(ShowSettings()))

        menuResearch = bar.addMenu("Search")
        menuResearch.addAction("Advanced search").triggered.connect(lambda: self.emit(ShowFrame(AdvancedSearch)))
        menuResearch.addAction("Standard search").triggered.connect(lambda: self.emit(ShowFrame(ResearchWidget)))

    def initWidget(self):
        mainWidget = QWidget(self)  # central placeholder widget
        self.setCentralWidget(mainWidget)
        mainWidget.setMinimumSize(700, 800)
        content = QGridLayout(mainWidget)

        # main component area (stacked widget)
        self.componentArea = ComponentArea(self.gui, mainWidget)
        self.componentArea.emit = lambda e: self.gui.emit(e)
        self.componentArea.gui = self.gui
        self.gui.registerListener(self.componentArea)

        # Search bar
        # search bar will be shown by default, you may disable it by emitting HideSearch
        recherche = ResearchWidget(mainWidget)
        recherche.gui = self.gui
        recherche.emit = lambda e: self.gui.emit(e)
        self.search = recherche
        # Error widget
        self.errorWidget = ErrorWidget(self)

        # gridding
        content.addWidget(recherche, 1, 0)
        content.addWidget(self.componentArea, 2, 0)

        mainWidget.setLayout(content)

        self.main = mainWidget

    def addError(self, text):
        self.errorWidget.updateText(text)
        self.errorWidget.display()

    def handle(self, event):
        if isinstance(event, ErrorEvent):
            msg = "ERROR [{}] : {}".format(event.type, event.value)
            self.statusBar().showMessage(msg)
            self.addError(msg)
            QTimer.singletShot(2000, lambda: self.statusBar().showMessage(""))  # reset the message in 2 seconds
        elif isinstance(event, HideSearch):
            self.search.setHidden(True)
        elif isinstance(event, ShowSearch):
            self.search.setHidden(False)
