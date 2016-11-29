import sys

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListWidget
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

        self.initWidget()
        self.show()
        self.explorer = Explorer()

    def initWidget(self):
        content = QGridLayout(self)

        self.btnOpenDir = QPushButton("Select a directory to scan",self)
        self.lblLstParseFile = QLabel("list of the parsed files",self)
        self.lstFileParse = QListWidget(self)
        self.lblLstNotParseFile = QLabel("list of the parsed files", self)
        self.lstFileNotParse = QListWidget(self)

        self.lstFileParse.setFixedSize(650,200)
        self.lstFileNotParse.setFixedSize(650,200)

        content.addWidget(self.btnOpenDir,0,0)
        content.addWidget(self.lstFileNotParse,1,0)
        content.addWidget(self.lstFileParse,2,0)



        self.btnOpenDir.clicked.connect(self.chooseDir)
    def chooseDir(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')


        self.setLayout(content)



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

class FileWidget(QWidget):
    def __init__(self,parent = None):
        super(FileWidget,self).__init__(self,parent)
    def initWidget(self):
        pass

class ExplorerWidget(QWidget):
    def __init__(self,parent = None):
        super(ExplorerWidget,self).__init__(self,parent)
    def initWidget(self):
        pass

if __name__ == '__main__':
    pass
    # from app.gui.Qgui import Gui
    # Gui.start()
