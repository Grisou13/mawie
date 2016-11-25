import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt
from app.gui.components.QMovieListWidget import ResearchListFrame
from app.gui.components.QMovieWidget import MovieFrame
from app.gui.components.QResearchWidget import  ResearchFrame
from app.explorer.explorer import Explorer

from app.helpers import SingletonMixin
import weakref
from app.gui.components import GuiComponent

class NotAComponent(Exception):
    pass


class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur
        self.components = weakref.WeakValueDictionary()
        self.initUI()

    def initUI(self):
        grid = QGridLayout(self)

        self.setFixedSize(700,800)
        self.center()

        self.setWindowTitle('Find My movie')
        recherche = ResearchFrame(self)

        stackWidget = QStackedWidget(self)
        stackWidget.setMinimumSize(700,700)

        listMovie = ResearchListFrame(stackWidget,self)
        movie = MovieFrame(stackWidget)

        stackWidget.addWidget(movie)
        stackWidget.addWidget(listMovie)
        stackWidget.setCurrentWidget(listMovie)

        grid.addWidget(recherche)
        grid.addWidget(stackWidget)
        self.setLayout(grid)
        self.show()
    @staticmethod
    def start():
        app = QApplication(sys.argv)
        ex = Gui()
        sys.exit(app.exec_())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def register_listener(self, cls):
        if not isinstance(cls, GuiComponent):
            raise NotAComponent("The class "+str(cls)+" should be extending GuiComponent")
        self.listeners[cls] = 1

    def dispatchAction(self, actionName, actionData):
        for l in self.listeners.keys():
            #print("from gui")
            #print(l.__class__)
            #print(id(l))
            #print()
            l.handleAction(actionName, actionData)

    def requestAction(self, originClass, actionName):
        for l in self.listeners.keys():
            if isinstance(l, originClass): continue  # we don't request on the same object... would be pointless
            originClass.handleAction("request_" + actionName, l.requestAction(actionName))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())

