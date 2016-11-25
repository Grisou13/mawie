import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QVBoxLayout
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt


class ResearchFrame(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initFrame()

    def initFrame(self):
        self.createWidget()
        self.show()

    def createWidget(self):
        grid = QGridLayout(self)
        self.lbl = QLabel("Please enter a resarch", self)
        self.inputSearch = QLineEdit(self)
        self.inputSearch.setFixedWidth(300)
        self.btnOk = QPushButton("Launch the research", self)

        grid.addWidget(self.lbl,0,0)
        grid.addWidget(self.inputSearch,0,1)
        grid.addWidget(self.btnOk,0,2)

        self.setLayout(grid)