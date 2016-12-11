
import copy
import os
import sys
import weakref
from PyQt5 import QtGui

from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtCore import QPropertyAnimation

from PyQt5.QtCore import QResource
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt

from mawie.events import Eventable
from mawie.gui.components import GuiComponent
from mawie.gui.components.QResearchWidget import  ResearchFrame
from mawie.gui.components.QStackedWidget import ComponentArea
from mawie.helpers import SingletonMixin

import mawie.gui.resources.images

import qdarkstyle
import traceback

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
class Gui(QWidget,Eventable,SingletonMixin):
    def __init__(self,parent=None):
        super(Gui, self).__init__(parent)

        self._components = {}
        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur
        self.componentArea = ComponentArea(self)
        self.initUI()
        self.registerExceptions()
    def resizeEvent(self, QResizeEvent):
        self.componentArea.resize(QResizeEvent.size())
        super(Gui, self).resizeEvent(QResizeEvent)
        QResizeEvent.accept()

    def initUI(self):
        content = QGridLayout(self)

        self.setMinimumSize(700,800)
        self.center()
        recherche = ResearchFrame(self)
        #add = AddFilesWidget(self)
        self.setWindowTitle('Find My movie')
        self.errorWidget = ErrorWidget(self)
        content.addWidget(self.componentArea,2,0)
        content.addWidget(recherche, 1, 0)

        self.setLayout(content)
        self.show()

    def myCustomHandler(self,ErrorType, ErrorContext, TraceBack):
        print("Qt error found.")
        print("Error Type: " + str(ErrorType))
        print("Error Context: " + str(ErrorContext))
        traceback.print_exc()
        #print("Traceback: " + str(traceback.print_tb(TraceBack)))
        self.addError("Error [" + str(ErrorType) + "] : " + str(ErrorContext))
        # m = QMessageBox()
        # m.setText("Error : "+str(ErrorType))
        # m.exec()
        #e = ErrorWidget(Gui.instance(),ErrorType)

        # Error logging code
        # Error emailing code

        #os.execv(sys.executable, [sys.executable] + sys.argv)

    def ErrorHandling(self,ErrorType, ErrorValue, TraceBack):
        print("System error found.")
        print("Error Type: " + str(ErrorType))
        print("Error Value: " + str(ErrorValue))
        traceback.print_exc()
        #print("Traceback: " + str(traceback.print_tb(TraceBack)))
        self.addError("Error [" + str(ErrorType) + "] : " + str(ErrorValue))
        # m = QMessageBox()
        # m.setText("Error [" + str(ErrorType) + "] : " + str(ErrorValue))
        # m.exec()
        #e = ErrorWidget(Gui.instance(), ErrorType)
        # Error logging code
        # Error emailing code

        #os.execv(sys.executable, [sys.executable] + sys.argv)

    def addError(self,text):
        print("############")
        print("handling error")
        print("############")
        #self.errorWidget.show()
        self.errorWidget.updateText(text)
        self.errorWidget.display()


    def registerExceptions(self):
        sys.excepthook = self.ErrorHandling
        QtCore.qInstallMessageHandler(self.myCustomHandler)
    @staticmethod
    def start():

        app = QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        ex = Gui()

        code = 0
        try:
            #raise Exception("Test exception")
            code = app.exec()
        except:
            ex.initUI()
        sys.exit(code)


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
