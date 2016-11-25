
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QScrollBar,QScrollArea,QVBoxLayout,QListWidget,QListWidgetItem
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect



class ResearchListFrame(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initFrame()

    def initFrame(self):
        self.createWidgets()
        self.show()
    def createWidgets(self):
        grid = QGridLayout()

        list = QListWidget(self)
        list.setMinimumSize(670,700)

        for i in range(120):
            item = QListWidgetItem(list)
            itemW= ResultRow(self)
            item.setSizeHint(itemW.sizeHint())
            list.setItemWidget(item, itemW)

        self.setLayout(grid)

class ResultRow(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.initRow()
        self.setGeometry(QRect(0,0,700,160))
        # self.setMinimumSize(650,160)
        # self.setSizePolicy(650,160)

    def initRow(self):
        self.createWidgets()
        self.show()

    def createWidgets(self):
        grid = QGridLayout()

        imgPix = QPixmap('filmImg.jpg')
        lblImg = QLabel(self)

        lblImg.setPixmap(imgPix)

        lblProducer = QLabel("Director: -", self)
        lblActors = QLabel("Actor(s): -",self)
        lblRating = QLabel("IMDb Rating: ",self)
        btnSee = QPushButton("See info",self)



        #gridLayout.addWidget(test)
        lblImg.setFixedSize(100,160)
        lblImg.setScaledContents(True)  # fit image to label


        grid.addWidget(lblImg,0,0,3,2)
        grid.addWidget(lblProducer,0,2)
        grid.addWidget(lblRating, 1, 2)
        grid.addWidget(lblActors, 2, 2)
        grid.addWidget(btnSee, 0, 3,3,2)

        self.setLayout(grid)
