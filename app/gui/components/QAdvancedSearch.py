from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget


from app.research.research import Research


class QAdvancedSearch(QWidget):
    def __init__(self, parent = None, flags = None, *args, **kwargs):
        super().__init__(parent,flags, *args, **kwargs)
        self.data = {}
        self.search = Research()
        self.initWidget()
    def initWidget(self):
        fields = self.search.get_fields(self.search.model)
        print(fields)
        layout = QFormLayout(self)
        for f in fields:
            lbl = QLabel()
            lbl.setText(f)
            input = QLineEdit()
            input.setPlaceholderText(f)
            input.textChanged.connect(lambda t : self.updateData(f,t))
            layout.addRow(lbl,input)

        s = QPushButton()
        s.clicked.connect(self.query)
        self.setLayout(layout)
    def updateData(self,fieldName,text):
        self.data[fieldName] = text
    def query(self):
        self.search.search(self.data)
if __name__ == '__main__':
    from app.gui.Qgui import Gui
    Gui.start()