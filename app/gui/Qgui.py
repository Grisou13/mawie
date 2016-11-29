import copy
import os
import sys
import weakref

from PyQt5.QtCore import QResource
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt

from app.gui.components import GuiComponent
from app.gui.components.QExplorer import AddFilesWidget
from app.gui.components.QMovieListWidget import MovieListFrame
from app.gui.components.QMovieWidget import MovieFrame
from app.gui.components.QResearchWidget import  ResearchFrame
from app.gui.components.QStackedWidget import ComponentArea
from app.helpers import SingletonMixin

import app.gui.resources.images

class NotAComponent(Exception):
    pass

class Gui(QWidget,SingletonMixin):
    def __init__(self,parent=None):
        super(Gui, self).__init__(parent)
        self._components = {}
        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur
        self.componentArea = ComponentArea(self)

        resources =QResource()
        print(os.path.realpath(os.path.join("../../","conf/images.qrc")))
        resources.registerResource(os.path.realpath(os.path.join("../../","conf/images.qrc")))
        print(resources.data())

    def initUI(self):
        content = QGridLayout(self)

        self.setMinimumSize(700,800)
        self.center()
        recherche = ResearchFrame(self)
        add = AddFilesWidget(self)
        self.setWindowTitle('Find My movie')
        content.addWidget(self.componentArea,1,0)
        content.addWidget(recherche, 0, 0)
        content.addWidget(add, 0, 1)
        #self.componentArea = content

        self.setLayout(content)
        self.show()
    @staticmethod
    def start():
        app = QApplication(sys.argv)
        ex = Gui()
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
    def addComponent(self, cls):
        c = cls(self)
        if isinstance(c,GuiComponent):
            self._components[c.__class__.__name__] = c
            if isinstance(c,QWidget):
                self.componentArea.addWidget(c)

    def register_listener(self, cls):
        if not isinstance(cls, GuiComponent):
            raise NotAComponent("The class " + str(cls) + " should be extending GuiComponent")
        self.listeners[cls] = 1

    def dispatchAction(self, actionName, actionData = None):
        print("dispatching action : "+actionName )
        for l in self.listeners.keys():
            # print("from gui")
            # print(l.__class__)
            # print(id(l))
            # print()
            l.handleAction(actionName, actionData)
    def requestAction(self, originClass, actionName):
        for l in self.listeners.keys():
            if isinstance(l, originClass): continue  # we don't request on the same object... would be pointless
            originClass.handleAction("request_" + actionName, l.requestAction(actionName))



if __name__ == '__main__':
    Gui.start()
