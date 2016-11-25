import sys
from PyQt5.QtWidgets import QWidget, QLabel,QPushButton,QGridLayout,QScrollBar,QScrollArea,QVBoxLayout
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import QRect,Qt

class MovieFrame(QWidget):
    def __init__(self,parent, gui):
        super().__init__(parent)
        self.initFrame()

    def initFrame(self):
        self.createWidgets()
        self.show()

    def createWidgets(self):

        grid = QGridLayout()
        fontTitle = QFont('Arial',20)
        fontInfo = QFont('Arial',8)
        imgPix = QPixmap('filmImg.jpg')
        lblImg = QLabel(self)
        lblImg.setFixedSize(300, 465)
        lblImg.setScaledContents(True)

        lblTitle = QLabel("Saving Private Ryan",self)
        lblImg.setPixmap(imgPix)
        lblScenarist = QLabel("Writer : -", self)
        lblDirector = QLabel("Director: -", self)
        lblActors = QLabel("Actor(s): -",self)
        lblRuntime = QLabel("Runtime: -",self)
        lblRate = QLabel("IMDb Rate: -",self)
        lblAwards = QLabel("Awards : -",self)
        lblCountry = QLabel("Country : -",self)
        lblRelease = QLabel("Release date : -",self)
        lblPlot = QLabel("Plot: fight e grave telegrams on the same day. The United States Army Chief of Staff, George C. Marshall, is given an opportunity to alleviate some of her grief when he learns of a fourth brother, Private James Ryan, and decides to send out 8 men (Cpt. Miller and select members from 2nd Rangers) to find him and bring him back home to his mother..",self)

        #Set font to labels
        lblTitle.setFont(fontTitle)
        lblScenarist.setFont(fontInfo)
        lblDirector.setFont(fontInfo)
        lblActors.setFont(fontInfo)
        lblRuntime.setFont(fontInfo)
        lblRate.setFont(fontInfo)
        lblAwards.setFont(fontInfo)
        lblCountry.setFont(fontInfo)
        lblRelease.setFont(fontInfo)
        lblPlot.setFont(fontInfo)


        lblPlot.setWordWrap(True)
        lblTitle.setWordWrap(True)
        btnLauchnFilm = QPushButton("Launch Film",self)

        grid.addWidget(lblImg, 1, 0, 8, 0)

        grid.addWidget(lblTitle,0,0,1,2)
        grid.addWidget(lblScenarist,1,1)
        grid.addWidget(lblDirector,2,1)
        grid.addWidget(lblActors,3,1)
        grid.addWidget(lblRuntime,4,1)
        grid.addWidget(lblRate,5,1)
        grid.addWidget(lblAwards,6,1)
        grid.addWidget(lblCountry,7,1)
        grid.addWidget(lblRelease,8,1)
        grid.addWidget(lblPlot,9,0,1,2)
        grid.addWidget(btnLauchnFilm,10,0,2,2)
        self.setLayout(grid)