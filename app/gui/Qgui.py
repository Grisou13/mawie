import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QMainWindow,QStackedWidget
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt
from app.gui.components.QMovieListWidget import ResearchListFrame
from app.gui.components.QMovieWidget import MovieFrame
from app.gui.components.QResearchWidget import  ResearchFrame


class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout(self)

        self.setFixedSize(700,800)
        self.center()

        self.setWindowTitle('Find My movie')
        recherche = ResearchFrame(self)

        stackWidget = QStackedWidget(self)
        stackWidget.setMinimumSize(700,700)

        listMovie = ResearchListFrame(stackWidget)
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

#Créer la ligne du film


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())

