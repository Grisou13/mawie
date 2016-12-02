import sys
import os
from urllib.parse import urlparse

from PyQt5.QtCore import QRect
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
            lst, lstParsed, lstNotParsed = self.explorer.getFolderContent(self.dirPath)
            data=["c:/test/film2mer.de111","c:/test/film2mer.de222","c:/test/test33","c:/test/film2mer.de444","c:/test/film2mer.de55","c:/test/film2mer.de","c:/test/film2mer.de","c:/test/film2mer.de","c:/test/film2mer.de","C:\Program Files (x86)\Apple Software Update\SoftwareUpdate.Resources\\fr.lproj[ www.CpasBien.cm ] The.Walking.Dead.S06E15.PROPER.VOSTFR.WEB-DL.XviD-SDTEAM.avi"]
            print(len(lstParsed))
            self.lstFileNotParse.clear()
            for file in data:
                fPath = file
                try:
                    item = QListWidgetItem(self.lstFileNotParse)
                    itemW = FileNotParsedWidget(self, file)
                    item.setSizeHint(itemW.sizeHint())
                    self.lstFileNotParse.setItemWidget(item, itemW)
                    itemW.btnGiveImdbUrl.clicked.connect(lambda ignore, widgetListItem=item, filePath=file:
                                                         self.getFilmInfoByUrl(widgetListItem,filePath))
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
        self.dirPath = QFileDialog.getExistingDirectory(self, 'Open file', 'C:/Users/ilias.goujgali/Videos',QFileDialog.ShowDirsOnly)
        self.inputPath.setText(self.dirPath)

    def getFilmInfoByUrl(self,item,file):
        idMovie = None
        url = None
        urlPath = None
        itemAdd= None #item of the QListWidget use for add not parsed file list to parsed file list

        url, ok = QInputDialog.getText(self,'Copy IMDb URL', 'Please copy the URL of the web page IMDb of the movie:')
        if url is not None:
            urlParsed = urlparse(url)
            urlPath = urlParsed.path
            idMovie = urlPath.split("title/")[1][:-1]

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
    def __init__(self,parent,file=None):
        super().__init__(parent)
        self.file = file
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



class ExplorerWidget(QWidget):
    def __init__(self,parent = None):
        super(ExplorerWidget,self).__init__(self,parent)
    def initWidget(self):
        pass

if __name__ == '__main__':
    from app.gui.Qgui import Gui
    Gui.start()