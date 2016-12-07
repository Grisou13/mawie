from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                 QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QDialog


class VideoPlayer(QDialog):
    def __init__(self, parent=None, path = None):
        super(VideoPlayer, self).__init__(parent)
        moviePath = path
        #moviePath='C:/Users/ilias.goujgali/Videos/Wildlife.wmv'
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(moviePath)))
        self.mediaPlayer.setVolume(100)
        self.videoWidget = VideoWidget()
        self.resize(1000, 700)
        self.show()

        self.playButton = QPushButton("Play")
        self.btnFullScreen = QPushButton("Full screen", self)
        self.btnFullScreen.clicked.connect(self.fullScreen)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0,100)
        self.volumeSlider.setValue(100)

        self.volumeSlider.sliderMoved.connect(self.setVolume)





        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 0, 0)
        layoutH.addWidget(self.playButton)
        layoutH.addWidget(self.positionSlider)
        layoutH.addWidget(self.volumeSlider)
        layoutH.addWidget(self.btnFullScreen)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addLayout(layoutH)



        self.setLayout(layout)
        self.playButton.clicked.connect(self.play)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)




    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setText("Pause")
        else:
            self.playButton.setText("Play")

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        print(duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)


    def setVolume(self,position):
        self.mediaPlayer.setVolume(position)

    def fullScreen(self):
        self.videoWidget.fullScreen()

class VideoWidget(QVideoWidget):
    def __init__(self):
        super(VideoWidget, self).__init__()

    def fullScreen(self):
        self.setFullScreen(True)

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            print("test")
            self.setFullScreen(False)
    def mouseDoubleClickEvent(self, *args, **kwargs):
        if self.isFullScreen() is True:
            self.setFullScreen(False)
            self.setCursor(Qt.OpenHandCursor)
        else:
            self.setFullScreen(True)
            self.setCursor(Qt.BlankCursor)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    player = VideoPlayer()
    sys.exit(app.exec_())