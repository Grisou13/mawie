
import copy
import os
import sys
import weakref
from PyQt5 import QtGui

from PyQt5 import QtCore

from PyQt5.QtCore import QResource
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt

from app.events import Eventable
from app.gui.components import GuiComponent
from app.gui.components.QResearchWidget import  ResearchFrame
from app.gui.components.QStackedWidget import ComponentArea
from app.helpers import SingletonMixin

import app.gui.resources.images

import qdarkstyle

class NotAComponent(Exception):
    pass

class ErrorWidget(QWidget):
    def __init__(self,parent = None, exception = None):
        super(ErrorWidget, self).__init__(parent)
        self.setWindowOpacity(0.0)
        QTimer.singleShot(1000,self.reveal)

        lbl = QLabel(self)
        lbl.setStyleSheet("""
                        QLabel{
                            background-color:yellow;
                            border-color:yellow;
                            border-radius:5px;
                            border-width: 1px;
                            border-style: solid;
                        }
                        """)
        lbl.setText(str(exception))
        lbl.show()
        self.show()
        print("showing error widget")
    def reveal(self):
        self.setWindowOpacity(1.0)
        self.move(0,self.height())
        print("shown")
        QTimer.singleShot(5000, self.delete)
    def delete(self):
        print("deleted")
        #self.parent.removeWidget(self)
        self.deleteLater()
class Gui(QWidget,Eventable,SingletonMixin):
    def __init__(self,parent=None):
        super(Gui, self).__init__(parent)
        self.registerExceptions()
        self._components = {}
        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur
        self.componentArea = ComponentArea(self)
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
        self.errorWidget = QLabel(self)
        self.errorWidget.setVisible(False)
        content.addWidget(self.errorWidget,0,0)
        content.addWidget(self.componentArea,2,0)
        content.addWidget(recherche, 1, 0)
        #content.addWidget(add, 0, 1)

        self.setLayout(content)
        self.show()

    def myCustomHandler(self,ErrorType, ErrorContext, TraceBack):
        print("Qt error found.")
        print("Error Type: " + str(ErrorType))
        print("Error Context: " + str(ErrorContext))
        print("Error traceback: "+ str(TraceBack))
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
        print("Traceback: " + str(TraceBack))
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
        self.errorWidget.setText(text)
        self.errorWidget.setVisible(True)
        self.errorWidget.show()
        QTimer.singleShot(5000, lambda :self.errorWidget.setVisible(False))
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
            ex.initUI()
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
