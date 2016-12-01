from PyQt5.QtGui import QPixmap

import app.gui.resources
from PyQt5.QtCore import QDirIterator
d = QDirIterator(":",QDirIterator.Subdirectories)
while d.hasNext():
    print(d.next())

