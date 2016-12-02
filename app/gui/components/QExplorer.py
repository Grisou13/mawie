import sys
import os
from urllib.parse import urlparse

from PyQt5.QtCore import QRect
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

from app.explorer.explorer import Explorer
from app.gui.components import GuiComponent

#dir_ = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
class AddFilesWidget(QWidget, GuiComponent):
    def __init__(self, parent,gui):
        super(AddFilesWidget,self).__init__(parent)
        self.gui = gui
        self.gui.register_listener(self)
        self.dirPath = None

        self.initWidget()
        self.show()
        self.explorer = Explorer()

    def initWidget(self):
        content = QGridLayout(self)
        self.inputPath = QLineEdit(self,placeholderText="No selected folder")
        self.inputPath.setReadOnly(True)
        self.btnOpenDir = QPushButton("Select a directory to scan",self)
        self.btnScan = QPushButton("Scan directory",self)


        self.lblLstParseFile = QLabel("list of the parsed files",self)
        self.lstFileParse = QListWidget(self)

        self.lblLstNotParseFile = QLabel("list of the parsed files", self)
        self.lstFileNotParse = QListWidget(self)
        self.lstFileParse.setFixedSize(660,200)
        self.lstFileNotParse.setFixedSize(660,200)

        content.addWidget(self.inputPath, 0, 0)
        content.addWidget(self.btnOpenDir,0,1)
        content.addWidget(self.btnScan,0,2)
        content.addWidget(self.lblLstParseFile,1,0)
        content.addWidget(self.lstFileNotParse,2,0)
        content.addWidget(self.lblLstNotParseFile,3,0)
        content.addWidget(self.lstFileParse,4,0)

        self.setLayout(content)

        self.btnOpenDir.clicked.connect(self.chooseDir)
        self.btnScan.clicked.connect(self.scanDir)
    def scanDir(self):
        if  self.dirPath is not None:
            explo = Explorer(self.dirPath)
            explo.getFolderContent()
            data=["c:/test/film2mer.de","c:/test/film2mer.de","c:/test/film2mer.de","c:/test/film2mer.de","c:/test/film2mer.de","c:/test/film2mer.de","c:/test/film2mer.de","c:/test/film2mer.de","c:/test/film2mer.de","C:\Program Files (x86)\Apple Software Update\SoftwareUpdate.Resources\\fr.lproj[ www.CpasBien.cm ] The.Walking.Dead.S06E15.PROPER.VOSTFR.WEB-DL.XviD-SDTEAM.avi"]

            self.lstFileNotParse.clear()
            for file in data:
                fPath = file
                try:
                    item = QListWidgetItem(self.lstFileNotParse)
                    itemW = FileNotParsedWidget(self, file)
                    item.setSizeHint(itemW.sizeHint())
                    self.lstFileNotParse.setItemWidget(item, itemW)
                    itemW.btnGiveImdbUrl.clicked.connect(lambda ignore, x=fPath: self.getFilmInfoByUrl(x))
                except Exception as e:
                    print(e)

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
        self.dirPath = QFileDialog.getExistingDirectory(self, 'Open file', 'c:\\',QFileDialog.ShowDirsOnly)
        self.inputPath.setText(self.dirPath)

    def getFilmInfoByUrl(self,file):
        url, ok = QInputDialog.getText(self,'Copy IMDb URL', 'Please copy the URL of the web page IMDb of the movie:')
        urlParsed = urlparse(url)
        netLoc = urlParsed.netloc
        imdbUrl = 'www.imdb.com'
        urlPath = urlParsed.path
        idMovie = urlPath.split("title/")[1][:-1]
        print(idMovie)
        # if netLoc is not imdbUrl:
        #     msgBox = QMessageBox()
        #     msgBox.setIcon(QMessageBox.Critical)
        #     msgBox = QMessageBox()
        #     msgBox.setIcon(QMessageBox.Critical)
        #     msgBox.setText("This URL isn't from IMDb")
        #     msgBox.setWindowTitle("This Url isn't valid")
        #     msgBox.setStandardButtons(QMessageBox.Ok)
        #     msgBox.exec()
        # else:
        #     print("ntm")




        # content = QGridLayout(self)
        # btn = QPushButton()
        # btn.setText("add")
        # btn.clicked.connect(self.toggleButtons)
        # content.addWidget(btn,0,0,1,2)
        # directoryBtn = QPushButton()
        # directoryBtn.clicked.connect(self.addDirectory)
        # directoryBtn.setText("Directory")
        # directoryBtn.setVisible(False)
        # content.addWidget(directoryBtn,1,0)
        # self.leftBtn = directoryBtn
        # #button will appear on the left
        # # directoryBtn.x = btn.x() - directoryBtn.width()/2 - 10 #just add 10 for margin
        # # directoryBtn.y = btn.y() + 2#
        # fileBtn = QPushButton()
        # fileBtn.setText("File")
        # fileBtn.setVisible(False)
        # content.addWidget(fileBtn,1,1)
        # self.rightBtn = fileBtn
        # #self.leftBtn.show()
        # #self.rightBtn.show()
        # self.setLayout(content)

    def toggleButtons(self):
        self.leftBtn.setVisible(not self.leftBtn.isVisible())
        self.rightBtn.setVisible(not self.rightBtn.isVisible())

    def addDirectory(self):
        self.toggleButtons()
        Gui.instance().dispatchAction("show-directory-list")
        dir_ = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        if dir_ is not None and dir_ is not "":
            self.explorer.getFolderContent(dir_)
            Gui.instance().dispatchAction("parsed-list",self.explorer.parsedFiles)
            Gui.instance().dispatchAction("non-parsed",self.explorer.nonParsedFiles)

    def handleAction(self, actionName, data):
        pass
    def requestAction(self,name):
        pass
class FileParsedWidget(QWidget):
    def __init__(self, parent, file=None):
        super().__init__(parent)
        self.file = file
        self.createWidgets()

    def createWidgets(self):
        grid = QGridLayout()
        lblTitle = QLabel("")
        lblFile = QLabel(self.file, self)
        self.btnGiveImdbUrl = QPushButton("Give IMDb url", self)

        lblFile.setFixedWidth(200)
        lblFile.setWordWrap(True)

        grid.addWidget(lblFile, 0, 1)
        grid.addWidget(self.btnGiveImdbUrl, 0, 2)
        self.setLayout(grid)
class DirectoryListWidget(QWidget, GuiComponent):
    def __init__(self,parent = None):
        super(DirectoryListWidget,self).__init__(parent)

    def initWidget(self):
        grid = QGridLayout()
        parsedList = QListWidget(self)
        nonParsedList = QListWidget(self)
        grid.addWidget(parsedList)
        grid.addWidget(nonParsedList)
        self.setLayout(grid)

    def addParsed(self,list):
        pass

    def addParsingError(self,list):
        pass

    def handleAction(self, actionName, data):
        if actionName == "parsed-list":
            self.addParsed(data)
        if actionName == "non-parsed":
            self.addParsingError(data)

    def requestAction(self,name):
        pass

class FileNotParsedWidget(QWidget):
    def __init__(self,parent,file=None):
        super().__init__(parent)
        self.file = file
        self.createWidgets()

    def createWidgets(self):
        grid = QGridLayout()
        lblFile = QLabel(self.file,self)
        self.btnGiveImdbUrl = QPushButton("Give IMDb url",self)


        lblFile.setFixedWidth(400)
        lblFile.setWordWrap(True)

        grid.addWidget(lblFile,0,1)
        grid.addWidget(self.btnGiveImdbUrl,0,2)
        self.setLayout(grid)

class ExplorerWidget(QWidget):
    def __init__(self,parent = None):
        super(ExplorerWidget,self).__init__(self,parent)
    def initWidget(self):
        pass

if __name__ == '__main__':
    from app.gui.Qgui import Gui
    Gui.start()