import sys
import os
from urllib.parse import urlparse

from PyQt5.QtCore import QRect, QRunnable, QThreadPool, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.uic.properties import QtGui
from PyQt5.QtWidgets import QFileDialog
import qtawesome as qta
from six import unichr

from mawie.events.gui import ShowExplorer
from mawie.explorer.explorer import Explorer
from mawie.gui.components import GuiComponent
from mawie.events import *
from mawie.events.explorer import *
import time
import sys
import traceback
import copy

class ExplorerRun(QThread):
    def __init__(self, explorer, path, parent = None):
        super(ExplorerRun,self).__init__(parent)
        self.setPriority(QThread.IdlePriority)
        print("new thread started")
        self.toParse = path
        self.explorer = copy.deepcopy(explorer) #redundant, maybe use a singleton?

    def run(self):
        try:
            for m in self.explorer.getMoviesFromPath(self.toParse):
                pass
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            print(sys.exc_info())


class FileParsedListWidget(QListWidget,Listener):
    def __init__(self,parent = None):
        super(FileParsedListWidget,self).__init__(parent)
    def handle(self,event):
        if isinstance(event,MovieParsed):
            self.addItem(event.data)
    def addItem(self,file_):
        item = QListWidgetItem(self)
        itemW = FileParsedWidget(self, file_["title"])
        item.setSizeHint(itemW.sizeHint())
        self.setItemWidget(item, itemW)
        time.sleep(.5)

class FileNotParsedListWidget(QListWidget,Listener):
    def __init__(self,parent):
        super(FileNotParsedListWidget,self).__init__(parent)
    def handle(self,event):
        if isinstance(event,MovieNotParsed):
            self.addItem(event.data)
    def addItem(self,file_):
        item = QListWidgetItem(self)
        itemW = FileNotParsedWidget(self, file_["filePath"])
        item.setSizeHint(itemW.sizeHint())
        self.setItemWidget(item, itemW)
        time.sleep(.5)

#dir_ = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
class AddFilesWidget(GuiComponent):
    def __init__(self, parent):
        super(AddFilesWidget,self).__init__(parent)
        self.dirPath = None
        self.explorer = Explorer()

        self.initWidget()
        self.show()

    def initWidget(self):
        content = QGridLayout(self)
        self.inputPath = QLineEdit(self,placeholderText="No folder selected")
        self.inputPath.setReadOnly(True)

        self.btnOpenDir = QPushButton("Select a directory to scan")
        self.btnScan = QPushButton("Scan directory")


        self.lblLstParseFile = QLabel("list of parsed files")
        #self.lstFileParse = QListWidget(self)
        self.lstFileParse = FileParsedListWidget(self)
        self.explorer.registerListener(self.lstFileParse)

        self.lblLstNotParseFile = QLabel("list of  non parsable files")
        self.lstFileNotParse = FileNotParsedListWidget(self)
        self.explorer.registerListener(self.lstFileNotParse)
        #self.lstFileNotParse = QListWidget(self)
        self.lstFileParse.setMinimumSize(660,200)
        self.lstFileNotParse.setMinimumSize(660,200)

        content.addWidget(self.inputPath, 0, 0)
        content.addWidget(self.btnOpenDir,0,1)
        #content.addWidget(self.btnScan,0,2)
        content.addWidget(self.lblLstNotParseFile,1,0)
        content.addWidget(self.lstFileNotParse,2,0,1,3)
        content.addWidget(self.lblLstParseFile,3,0)
        content.addWidget(self.lstFileParse,4,0,1,3)



        self.setLayout(content)

        self.btnOpenDir.clicked.connect(self.chooseDir)
        #self.btnScan.clicked.connect(self.scanDir)
    def _scanFile(self):
        pass
    def scanDir(self):
        if  self.dirPath is not None:
            if os.path.isdir(self.dirPath):

                runnable = ExplorerRun(self.explorer,self.dirPath)
                runnable.run()
                #QThreadPool.globalInstance().start(runnable) # execute the explorer in a seperate thread, or just let Qt handle it
                #lst = self.explorer.getMoviesFromPath(self.dirPath)
                # data=["c:/test/film2mer.de111","c:/test/film2mer.de222","c:/test/test33","c:/test/film2mer.de444","c:/test/film2mer.de55","c:/test/film2mer.de","c:/test/film2mer.de","c:/test/film2mer.de","c:/test/film2mer.de","C:\Program Files (x86)\Apple Software Update\SoftwareUpdate.Resources\\fr.lproj[ www.CpasBien.cm ] The.Walking.Dead.S06E15.PROPER.VOSTFR.WEB-DL.XviD-SDTEAM.avi"]
                # print(len(lst))
                # self.lstFileNotParse.clear()
                # for f in lst:
                #     print(f)
                #     fPath = f["filePath"]
                #     item = QListWidgetItem(self.lstFileNotParse)
                #     itemW = FileNotParsedWidget(self, f["title"])
                #     item.setSizeHint(itemW.sizeHint())
                #     self.lstFileNotParse.setItemWidget(item, itemW)
                #     itemW.btnGiveImdbUrl.clicked.connect(lambda ignore, widgetListItem=item, filePath=f["filePath"]:
                #                                          self.getFilmInfoByUrl(widgetListItem,filePath))


        else:
            print("No folder")
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("You don't have selected any folder")
            msgBox.setWindowTitle("No folder selected")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    def chooseDir(self):
        self.dirPath = QFileDialog.getExistingDirectory(self, 'Open file', 'C:/Users/ilias.goujgali/Videos',QFileDialog.ShowDirsOnly)
        self.inputPath.setText(self.dirPath)
        self.scanDir()

    def getFilmInfoByUrl(self,item,file):
        """
        TODO move this to nonparsedlist component
        """
        idMovie = None
        url = None
        urlPath = None
        itemAdd= None

        url, ok = QInputDialog.getText(self,'Copy IMDb URL', 'Please copy the URL of the web page IMDb of the movie:')
        if url is not None and url != "":
            urlParsed = urlparse(url)
            urlPath = urlParsed.path
            idMovie = urlPath.split("title/")[1][:-1]
            #print(idMovie)

            if idMovie is not None or idMovie is not "":
                print(idMovie)
                row = self.lstFileNotParse.row(item)
                self.lstFileNotParse.takeItem(row)
                itemAdd = QListWidgetItem(self.lstFileParse)
                itemW = FileParsedWidget(self, file)
                itemAdd.setSizeHint(itemW.sizeHint())
                self.lstFileParse.setItemWidget(itemAdd, itemW)

                # TODO: add file to a database
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText("This url isn't valid")
                msgBox.setWindowTitle("We can't find the id of the movie, "
                                      "please enter an URL like http://www.imdb.com/title/tt0120815")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()


    def toggleButtons(self):
        self.leftBtn.setVisible(not self.leftBtn.isVisible())
        self.rightBtn.setVisible(not self.rightBtn.isVisible())

    def addDirectory(self):
        self.toggleButtons()
        self.gui.dispatchAction("show-directory-list")
        dir_ = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        if dir_ is not None and dir_ is not "":
            self.explorer.getFolderContent(dir_)
            self.gui.dispatchAction("parsed-list",self.explorer.parsedFiles)
            self.gui.dispatchAction("non-parsed",self.explorer.nonParsedFiles)
    def handle(self,event):
        super().handle(event)
        if isinstance(event, ShowExplorer):
            self.emit(ShowFrame(self))

    def handleAction(self, actionName, data):
        pass
    def requestAction(self,name):
        pass


class FileParsedWidget(QWidget):
    def __init__(self, parent, file_=None):
        super().__init__(parent)
        self.file = file_
        self.createWidgets()

    def createWidgets(self):
        content = QGridLayout()
        lblFile = QLabel(self.file, self)
        label = QLabel(unichr(0xf00c))
        label.setFont(qta.font('fa', 16))
        label.setStyleSheet("QLabel {color : green}")




        # = QLabel(self,faIconCheck)

        # styling_icon = qta.icon('fa.music',
        #                         active='fa.legal',
        #                         color='blue',
        #                         color_active='orange')
        # music_button = QtGui.QPushButton(styling_icon, 'Styling')


        # imgPath = os.path.join(os.path.realpath(__file__),"../../../../",".cache","ok.png")
        # lblImgValid.setPixmap(QPixmap(imgPath))

        lblFile.setFixedWidth(550)
        lblFile.setWordWrap(True)

        content.addWidget(lblFile, 0, 0)
        content.addWidget(label, 0, 1)
        self.setLayout(content)

class FileNotParsedWidget(QWidget):
    def __init__(self,parent,file_=None):
        super().__init__(parent)
        self.file = file_
        self.createWidgets()

    def createWidgets(self):
        grid = QGridLayout()
        lblFile = QLabel(self.file,self)
        print(self.file)
        faIconCheck = qta.icon("fa.external-link")
        self.btnGiveImdbUrl = QPushButton(faIconCheck,"Give IMDb URL",self)

        lblFile.setFixedWidth(400)
        lblFile.setWordWrap(True)

        grid.addWidget(lblFile,0,1)
        grid.addWidget(self.btnGiveImdbUrl,0,2)
        self.setLayout(grid)


class ExplorerWidget(GuiComponent):
    def __init__(self,parent):
        super(ExplorerWidget,self).__init__(parent)
        self.gui = parent.gui
        self.initWidget()

    def initWidget(self):
        self.add = AddFilesWidget(self)
        self.show()
if __name__ == '__main__':
    from mawie.gui.Qgui import start, ShowMovieList, ShowFrame

    start()
