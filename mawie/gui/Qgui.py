
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
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt

from mawie import App
from mawie.events import Eventable, Start
from mawie.gui.components import GuiComponent
from mawie.gui.components.QResearchWidget import  ResearchFrame
from mawie.gui.components.QStackedWidget import ComponentArea
from mawie.helpers import SingletonMixin

import mawie.gui.resources.images

import qdarkstyle
import traceback
from mawie.events.gui import *
class NotAComponent(Exception):
    pass

class ErrorWidget(QWidget):
    def __init__(self,parent = None):
        super(ErrorWidget, self).__init__(parent)
        self.errorWidget = QLabel(self)
        if parent is None:
            width = 500
        else:
            width = parent.width()
        self.errorWidget.setStyleSheet("""
                            QLabel{
                                width:%s;
                                color:#1E8BC3;
                                width:inherit;
                                background-color:black;
                                border-color:#6BB9F0;
                                font-weight:bold;
                                font-size:16px;
                                border-bottom-right-radius:5px;
                                border-bottom-left-radius:5px;
                                border-width: 1px;
                                border-style: solid;

                            }
                        """ % width)
        self.errorWidget.setFixedSize(width, self.errorWidget.font().pointSize()*4)
        self.errorWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.errorWidget.resizeEvent = self.resizeLabel
        #self.errorWidget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.errorWidget.setVisible(False)

        self.animationProp = b"opacity"  #needs to be in bytes... pyqt you know?
    def updateText(self,txt):
        self.errorWidget.setText(txt)
    def display(self):
        self.fadeIn()
        QTimer.singleShot(5000, lambda: self.fadeOut())

    def resizeLabel(self, evt):
        font = self.font()
        font.setPixelSize(self.height() * 0.8)
        self.setFont(font)

    def fadeIn(self):
        g = QGraphicsOpacityEffect(self)
        self.errorWidget.setGraphicsEffect(g)
        a = QPropertyAnimation(g, self.animationProp,self)
        a.setDuration(350)
        a.setStartValue(0)
        a.setEndValue(1)
        a.setEasingCurve(QEasingCurve.InBack)
        #a.valueChanged.connect(lambda:self.errorWidget.show())
        self.errorWidget.show()
        a.start()
    def fadeOut(self):
        g = QGraphicsOpacityEffect(self)
        self.errorWidget.setGraphicsEffect(g)
        a = QPropertyAnimation(g, self.animationProp,self)
        a.setDuration(350)
        a.setStartValue(1)
        a.setEndValue(0)
        a.setEasingCurve(QEasingCurve.OutBack)
        a.finished.connect(lambda : self.errorWidget.setVisible(False))
        a.start(QPropertyAnimation.DeleteWhenStopped)


class Gui(QMainWindow, Eventable):
    #based out of tornado ioloop https://github.com/tornadoweb/tornado/blob/master/tornado/ioloop.py
    _instance_lock = threading.Lock()
    @staticmethod
    def instance():
        print("getting instance")
        if not hasattr(Gui, "_instance"):
            with Gui._instance_lock:
                if not hasattr(Gui, "_instance"):
                    # New instance after double check
                    Gui._instance = Gui()
        return Gui._instance

    def __init__(self):
        super(Gui, self).__init__()
        print("starting gui")

        self.registerExceptions()

        print("done 1")
        self.initUI()
        print("done 2")

    def initUI(self):
        self.statusBar().showMessage("hi")
        print("starting ui")
        mainWidget = QWidget(self)
        mainWidget.gui = self
        self.main = mainWidget
        self.setCentralWidget(self.main)
        print("new main widget")
        content = QGridLayout(mainWidget)
        self.componentArea = ComponentArea(mainWidget)
        print("created component area")
        mainWidget.setMinimumSize(700,800)
        self.center()
        recherche = ResearchFrame(mainWidget)
        self.registerListener(recherche)
        self.setWindowTitle('Find My movie')
        self.errorWidget = ErrorWidget(self)
        content.addWidget(self.componentArea,2,0)
        content.addWidget(recherche, 1, 0)

        mainWidget.setLayout(content)

        print("showing widgerts")


        self.show()
        self.main.show()

    def errorHandling(self,ErrorType, ErrorValue, TraceBack):
        print("System error found.")
        print("Error Type: " + str(ErrorType))
        print("Error Value: " + str(ErrorValue))
        if isinstance(TraceBack,str):
            print("Error: "+TraceBack)
        else:
            traceback.print_exc()
        #self.emit(ErrorEvent(ErrorType,ErrorValue,TraceBack))
        self.addError("Error [" + str(ErrorType) + "] : " + str(ErrorValue))

    def addError(self,text):
        self.errorWidget.updateText(text)
        self.errorWidget.display()

    def registerExceptions(self):
        self.errorWidget = ErrorWidget(self)
        print("registering exception handlers")
        sys.excepthook = self.errorHandling
        QtCore.qInstallMessageHandler(self.errorHandling)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def handle(self, event):
        print("asdasd")
        if isinstance(event,Start):
            print("starting")
            self.initUI()
            self.backgroundApp = App.instance()
        elif isinstance(event,ShowFrame):
            if isinstance(event.data,str):
                pass #should redispatch an event for callin g the right class
        else:
            self.sendToBackground(event)

    def sendToBackground(self,event):
        print("sending to background")
        self.backgroundApp.newEvent.emit(event)


def start():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = Gui.instance()
    #ex.emit(Start())
    code = 0
    try:
        # raise Exception("Test exception")
        code = app.exec()
    except:
        ex.initUI()
    sys.exit(code)
if __name__ == '__main__':
    start()
