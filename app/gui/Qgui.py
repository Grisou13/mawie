import copy
import sys
import weakref

from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt

from app.gui.components import GuiComponent
from app.gui.components.QExplorer import AddFilesWidget
from app.gui.components.QMovieListWidget import ResearchListFrame
from app.gui.components.QMovieWidget import MovieFrame
from app.gui.components.QResearchWidget import  ResearchFrame
from app.helpers import SingletonMixin

class NotAComponent(Exception):
    pass

class Gui(QWidget,SingletonMixin):
    def __init__(self,parent=None):
        super(Gui, self).__init__(parent)
        self._components = {}
        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur
        stackWidget = QStackedWidget(self)
        stackWidget.setMinimumSize(700, 700)
        self.componentArea = stackWidget
    def initUI(self):
        content = QGridLayout(self)

        self.setFixedSize(700,800)
        self.center()
        recherche = ResearchFrame(self)
        add = AddFilesWidget(self)
        self.setWindowTitle('Find My movie')



        listMovie = ResearchListFrame(self.componentArea)
        movie = MovieFrame(self.componentArea)

        self.componentArea.addWidget(movie)
        self.componentArea.addWidget(listMovie)
        self.componentArea.setCurrentWidget(listMovie)
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
        ex.initUI()
        sys.exit(app.exec_())
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def addComponent(self, cls):
        if isinstance(cls,GuiComponent):
            self._components[cls.__class__.__name__] = cls
            if isinstance(cls,QWidget):
                self.componentArea.addWidget(cls)

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
#Créer la ligne du film


if __name__ == '__main__':
    Gui.start()

