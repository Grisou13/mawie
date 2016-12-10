import sys
import time
import asyncio

from PyQt5.QtWidgets import (QApplication, QProgressBar, QMainWindow, QSlider,
    QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QPushButton
from quamash import QEventLoop, QThreadExecutor



class MainWindow(QMainWindow):
    def __init__(self):
            super(MainWindow, self).__init__()

            self.progress = QProgressBar()
            self.progress.setRange(0, 99)
            self.progress.show()

            self.slider = QSlider()
            self.slider.show()

            # set layout
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.progress)
            self.layout.addWidget(self.slider)
            self.btn = QPushButton(parent=self)
            self.btn.setText("click me")
            self.btn.move(200,200)
            self.btn.show()
            self.win = QWidget()
            self.win.resize(320, 240)
            self.win.setLayout(self.layout)
            self.win.show()


            with loop:
                # context manager calls .close() when loop completes,
                # and releases all resources
                loop.run_until_complete(self.master())

    @asyncio.coroutine
    def master(self):
        yield from self.first_50()
        with QThreadExecutor(1) as exec:
            yield from loop.run_in_executor(exec, self.last_50)
        print('ready!')

    def updateValue(self, val):
        self.progress.setValue(val)

    @asyncio.coroutine
    def first_50(self):
        for i in range(50):
            self.updateValue(i)
            yield from asyncio.sleep(.05)

    def last_50(self):
        for i in range(50, 100):
            loop.call_soon_threadsafe(self.updateValue, i)
            time.sleep(.1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    main = MainWindow()
    main.show()
