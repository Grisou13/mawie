from PyQt5.QtCore import QEasingCurve
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget, QLabel
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
