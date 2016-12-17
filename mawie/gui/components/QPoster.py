
from PyQt5.QtCore import QDirIterator
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import PyQt5
from mawie.gui.components import Downloader
import mawie.gui.resources

class ImporterThread(QThread):
    """Class that actually downloads the image
        This class is actually the class that downloads the image from cache, internal mawie resources, or the internet
    """
    no_poster = ":/images/no-poster"
    result = pyqtSignal("QPixmap")
    def __init__(self, url, parent=None):
        super(ImporterThread, self).__init__(parent)
        if url is not None:
            self.url = url
        else:
            self.url = self.no_poster
        self.downloader = Downloader()
        self.downloader.downloaded.connect(self.downloadFinished)
        #self.image = QImage(self.no_poster)  # default the image to the no-poster

    def setUrl(self, url):
        self.url = url

    def run(self):
        """
        Runs the download and calls asyncronously the method ImporterThread.downloadFinished when the download of an external image was completed
        :return:
        """
        downloader = self.downloader
        try:
            path = QUrl(self.url)
            if self.url is not None and (self.url.startswith(":") or self.url.startswith("qrc://")):  # if it's a QRC image file, it's already built in the mawie... if everything was ok though
                self.downloader.resetDownloadData()
                self.downloadFinished()
            else:

                downloader.doDownload(path)
        except Exception as e:  # in case there isn't the internet or the url gives 404 error or bad url
            print("a problem with the connection or the url has occurred {" + e.with_traceback(e.__traceback__) + "}")

    def downloadFinished(self):
        data = self.downloader.downloadedData()
        image = QPixmap()
        if data is not None or len(data) >= 0:
            image.loadFromData(data)
        if image.isNull():
            image.load(self.no_poster)

        #broadcast the image, to all connected listeners
        self.result.emit(image)


class QPoster(QLabel):
    """
    Qposter is an image placeholder label, that uses a background thread to load the image. This allows a huge performance boost for the mawie
    """
    image_size = QSize(100,160)

    def __init__(self, parent=None, url=None):
        super(QPoster, self).__init__(parent)
        self.setScaledContents(True)
        self.setFixedSize(self.image_size)

        if url is None:
            self.setPixmap(QPixmap(ImporterThread.no_poster))
        self.thread = ImporterThread(url)
        self.thread.setUrl(url)
        self.thread.run()
        self.thread.result.connect(self._updateImage)

    def setDefaultImageSize(self, size):
        assert isinstance(size, tuple)
        self.image_size = size

    def updateUrl(self, url=None):
        self.thread.setUrl(url)
        self.thread.run()

    def _updateImage(self, image_):
        """
        This is connected to the download thread. Called only when the download thread has reaceived, or not an image
        :param image_:
        :type image_: QPixmap
        :return:
        """
        image_.scaled(self.image_size, PyQt5.QtCore.Qt.KeepAspectRatio)
        # image.scaledToHeight(self.image_size[1])
        # image.scaled(*self.image_size,Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(image_)
        self.show()


if __name__ == '__main__':
    from mawie.gui.Qgui import start

    start()
