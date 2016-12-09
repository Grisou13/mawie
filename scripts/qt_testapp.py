import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QPushButton


class MemoryButton(QPushButton):
    def __init__(self, *args, **kw):
        QPushButton.__init__(self, *args, **kw)
        self.last_mouse_pos = None
        self.clicked.connect(self.u)
    def mousePressEvent(self, event):
        self.last_mouse_pos = event.pos()
        QPushButton.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.last_mouse_pos = event.pos()
        QPushButton.mouseReleaseEvent(self, event)

    def get_last_pos(self):
        if self.last_mouse_pos:
            return self.mapToGlobal(self.last_mouse_pos)
        else:
            return None
    def u(self):
        popup = QMenu()
        #menu = popup.addMenu("Do Action")

        def _action(check):
            print("Action Clicked!")

        popup.addAction("Action").triggered.connect(_action)
        popup.exec(self.get_last_pos())
        #popup.exec(self.mapFromGlobal(QPoint(100,100)))
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.button = MemoryButton("Click Me!")
        self.button.show()
        self.show()



def testApp():
    app = QApplication(sys.argv)
    m = MainWindow()
    sys.exit(app.exec_())
if __name__ == '__main__':
    testApp()
