import logging

from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from sqlalchemy import Date

from mawie import models
from mawie.events.gui import ShowFrame
from mawie.events.search import SearchRequest
from mawie.gui.components import GuiComponent
from mawie.gui.components.QDateRangeInput import DateRangeInput
from mawie.gui.components.QMovieListWidget import MovieListWidget
from mawie.models.File import File
from mawie.models.Movie import Movie

log = logging.getLogger("mawie")


class AdvancedSearch(GuiComponent):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fields = ["name", "runtime", "genre", "release", "actors", "directors",
                       "filename"]  # TODO discover these directly with the research, for now just brutforce it
        # TODO make files and directories searchable
        self.model = Movie
        self.models = [Movie, File]
        self.data = {}
        self.initWidget()
        self.show()

    def initWidget(self):
        masterLayout = QBoxLayout(QBoxLayout.TopToBottom, self)
        for model in self.models:
            # self.data[model] = {}
            layout = QFormLayout(self)
            for f in models.get_fields(model):
                if "id" in f:  # we do not want users to be able to query id's (what would be the point?)
                    continue
                fieldType = models.find_type(model, f)
                lbl = QLabel()
                lbl.setText(f)
                if isinstance(fieldType, Date):
                    input = DateRangeInput(self, model, f)
                    input.valueChange.connect(lambda v, f=f, m=model: self.updateData(m, f, {"gte": v[0], "lte": v[1]}))
                    # layout.addRow(input)
                else:
                    input = QLineEdit()
                    input.setPlaceholderText(f)
                    input.textChanged.connect(lambda t, f=f, m=model: self.updateData(m, f, t))
                layout.addRow(lbl, input)
            masterLayout.addLayout(layout)
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            masterLayout.addWidget(separator)
        s = QPushButton()
        s.clicked.connect(self.query)
        s.setText("search")
        masterLayout.addWidget(s)
        self.setLayout(masterLayout)

    def updateData(self, model, fieldName, data):
        if data is not None:
            if not model in self.data:
                self.data[model] = {}
            self.data[model][fieldName] = data

    def query(self):
        if len(self.data.keys()) < 1:
            return
        # print(self.data)
        self.gui.emit(SearchRequest(self.data))
        self.gui.emit(ShowFrame(MovieListWidget.__name__))


if __name__ == '__main__':
    from mawie.gui import start

    start()
