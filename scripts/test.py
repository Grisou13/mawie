import sys
import time

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton

from app.gui.QtAsync import AsyncTask, coroutine
from PyQt5 import QtGui
from PyQt5.QtCore import QThread

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.cmd_button = QPushButton("Push", self)
        self.cmd_button.clicked.connect(self.send_evt)
        self.statusBar()
        self.show()

    def worker(self, inval):
        print("in worker, received '%s'" % inval)
        time.sleep(2)
        return "%s worked" % inval

    @coroutine
    def send_evt(self, arg):
        # out = AsyncTask(self.worker, "test string")
        # out2 = AsyncTask(self.worker, "another test string")
        #
        # print("kicked off async task, waiting for it to be done")
        # val = yield out
        # val2 = yield out2
        # print ("out is %s" % val)
        # print ("out2 is %s" % val2)
        out = yield AsyncTask(self.worker, "Some other string")
        print ("out is %s" % out)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = MainWindow()
    sys.exit(app.exec_())