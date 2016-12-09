from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget


class SettingsWidget(QWidget):
    def __init__(self,parent=None,gui=None):
        super(SettingsWidget, self).__init__(parent)
        self.gui = gui
        self.createWidgets()


    def createWidgets(self):
        grid = QGridLayout()
        font = QFont('Arial',22)
        settings = QSettings()

        settings.setValue("licornet",True)
        lblTitle= QLabel("Settings",self)
        lblTitle.setFont(font)
        chkDefaultSystemPlayer = QCheckBox("Only use default video player to play movie",self)
        chkUpdatorEnable = QCheckBox("Enabled updator",self)
        lblDeleteDb = QLabel("Delete the database : it will erase all the movie and associates files in the database",self)
        btnDeleteDb = QPushButton("Erase the database",self)



        lstFolder = QListWidget(self)
        grid.addWidget(lblTitle,0,0,1,2)
        grid.addWidget(chkDefaultSystemPlayer,1,0,1,2)
        grid.addWidget(chkUpdatorEnable,2,0,1,2)
        grid.addWidget(lblDeleteDb,3,0,1,1)
        grid.addWidget(btnDeleteDb,3,1,1,1)
        grid.addWidget(lstFolder,4,0,1,2)
        self.setLayout(grid)

class FolderList(QWidget):
    def __init__(self,parent,dir):
        super(FolderList, self).__init__()


# Movie - player par défault
# Explorer - Updator fréquence
# Explorer - Updator enabled/disabled
# First Launch - Create folders and stuff
# Erase database data V
# Folder deleting