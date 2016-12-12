import copy
import sys
import weakref

from PyQt5.QtCore import QCoreApplication
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
from PyQt5.QtCore import QSettings

class NotAComponent(Exception):
    pass

class Gui(QWidget,SingletonMixin):
    def __init__(self,parent=None):
        super(Gui, self).__init__(parent)
        self._components = {}
        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur
        self.componentArea = ComponentArea(self)


    def initUI(self):
        content = QGridLayout(self)

        self.setFixedSize(700,800)
        self.center()
        recherche = ResearchFrame(self)

        self.setWindowTitle('')

        content.addWidget(self.componentArea,1,0)
        content.addWidget(recherche, 0, 0)

        #self.componentArea = content

        self.setLayout(content)
        self.show()
    @staticmethod
    def start():
        app = QApplication(sys.argv)
        app.setOrganizationName("CPNV")
        app.setApplicationName("MAWIE")
        settings = QSettings()

        firstLaunch = settings.value("firstlaunch")
        updatorEnable = settings.value("updator/updatorEnable")
        frequency = settings.value("updator/frequency")
        playerDefault = settings.value("infomovie/player-default")

        if firstLaunch is None:
            settings.setValue("firstlaunch", True)
        if updatorEnable  is None:
            settings.setValue("updator/updatorEnable", True)
        if frequency is None:
            settings.setValue("updator/frequency",1800)
        if playerDefault is None:
            settings.setValue("infomovie/player-default",True)

        ex = Gui()
        ex.initUI()
        sys.exit(app.exec_())
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
