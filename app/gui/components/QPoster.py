from PyQt5 import QtCore

from PyQt5 import Qt
from PyQt5.QtCore import QFileInfo

from PyQt5.QtCore import QThread
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from app.gui.resources import *
from app.gui.components import Downloader


class ImporterThread(QThread):
    no_poster = ":/images/no-poster"
    result = pyqtSignal("QImage")

    def __init__(self, url, parent=None):
        super(ImporterThread, self).__init__(parent)
        self.url = url if url is not None else self.no_poster
        self.downloader = Downloader()
        #self.image = QImage(self.no_poster)  # default the image to the no-poster

    def setUrl(self, url):
        self.url = url

    def run(self):
        downloader = self.downloader
        try:
            path = QUrl(self.url)
            if self.url is not None and (self.url.startswith(":") or self.url.startswith("qrc://")):  # if it's a QRC image file, it's already built in the app... if everything was ok though
                print()
                print("image from qrc")
                print(QFileInfo(self.url).isBundle())
                image = QImage(self.url)
                self.result.emit(image)
            else:
                downloader.downloaded.connect(self.downloadFinished)
                downloader.doDownload(path)
        except Exception as e:  # in case there isn't the internet or the url gives 404 error or bad url
            print("a problem with the connection or the url has occurred {" + e.with_traceback(e.__traceback__) + "}")

    def downloadFinished(self):
        data = self.downloader.downloadedData()

        if data is not None or len(data) >= 0:
            image = QImage()
            image.loadFromData(data)
        else:
            image = QImage(self.no_poster)
        self.result.emit(image)


class QPoster(QLabel):
    """
    Qposter is an image placeholder label, that uses a background thread to load the image. This allows a huge performance boost for the app
    """
    image_size = (100, 160)

    def __init__(self, parent=None, url=None):
        super(QPoster, self).__init__(parent)
        self.setScaledContents(True)
        if url is None:
            self.setPixmap(QPixmap(ImporterThread.no_poster))
        self.thread = ImporterThread(url)
        self.thread.setUrl(url)
        self.thread.run()
        self.thread.result.connect(self._updateImage)
        self.show()
    def setDefaultImageSize(self, size):
        assert isinstance(size, tuple)
        self.image_size = size

    def updateUrl(self, url=None):
        self.thread.setUrl(url)
        self.thread.run()

    def _updateImage(self, image_):
        """
        updates the image from the ImporterThread.result signal
        :param image_:
        :return:
        """
        image = QPixmap()
        image.convertFromImage(image_)

        # image.scaledToHeight(self.image_size[1])
        # image.scaled(*self.image_size,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(image)

        self.show()


if __name__ == '__main__':
    from app.gui.Qgui import Gui

    Gui.start()
