
import copy
import os
import sys
import weakref
from PyQt5 import QtCore

from PyQt5.QtCore import QResource
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt

from app.events import Eventable
from app.gui.components import GuiComponent
from app.gui.components.QResearchWidget import  ResearchFrame
from app.gui.components.QStackedWidget import ComponentArea
from app.helpers import SingletonMixin

import app.gui.resources.images

class NotAComponent(Exception):
    pass

class Gui(QWidget,Eventable,SingletonMixin):
    def __init__(self,parent=None):
        super(Gui, self).__init__(parent)
        self._components = {}
        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur
        self.componentArea = ComponentArea(self)

    def initUI(self):
        content = QGridLayout(self)

        self.setMinimumSize(700,800)
        self.center()
        recherche = ResearchFrame(self)
        #add = AddFilesWidget(self)
        self.setWindowTitle('Find My movie')
        content.addWidget(self.componentArea,1,0)
        content.addWidget(recherche, 0, 0)
        #content.addWidget(add, 0, 1)

        self.setLayout(content)
        self.show()

    def myCustomHandler(ErrorType, ErrorContext):
        print("Qt error found.")
        print("Error Type: " + str(ErrorType))
        print("Error Context: " + str(ErrorContext))

        # Error logging code
        # Error emailing code

        os.execv(sys.executable, [sys.executable] + sys.argv)

    def ErrorHandling(ErrorType, ErrorValue, TraceBack, WhateverThisIs):
        print("System error found.")
        print("Error Type: " + str(ErrorType))
        print("Error Value: " + str(ErrorValue))
        print("Traceback: " + str(TraceBack))

        # Error logging code
        # Error emailing code

        os.execv(sys.executable, [sys.executable] + sys.argv)


    @staticmethod
    def start():

        app = QApplication(sys.argv)
        ex = Gui()
        sys.excepthook = ex.ErrorHandling
        QtCore.qInstallMessageHandler(ex.myCustomHandler)
        try:
            ex.initUI()
            c = app.exec_()
            sys.exit(c)
        except SystemExit as s:
            sys.exit()
        except Exception as e:
            print(e)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    # def addComponent(self, cls):
    #     #c = cls(self)
    #     self.register_listener(cls)
    #     if isinstance(cls,GuiComponent):
    #         self._components[cls.__class__.__name__] = c
    #         # if isinstance(c,QWidget):
    #         #     self.componentArea.addWidget(c)


if __name__ == '__main__':
    Gui.start()
