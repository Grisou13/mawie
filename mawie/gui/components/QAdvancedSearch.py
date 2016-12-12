import calendar
import json

import math
from PyQt5 import QtCore

from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QWidget
from sqlalchemy import Date
from sqlalchemy import distinct
from sqlalchemy import func
from datetime import date, datetime, time

from mawie import models
from mawie.gui.components import GuiComponent
from mawie.models.File import File
from mawie.models.Movie import Movie
from mawie.research.research import Research


class DateRangeInput(QWidget):
    valueChange = pyqtSignal(tuple)
    mysqlDateFormat = 'yyyy-MM-dd'
    @property
    def values(self):
        return self.minEdit.date().toString(self.mysqlDateFormat),self.maxEdit.date().toString(self.mysqlDateFormat)
    def __init__(self,parent = None, model = None, inputName = None,*arg,**kwargs):
        super().__init__(parent,*arg,**kwargs)
        if inputName is None : pass
        self.inputName = inputName
        self.data = {}

        v = model.query(func.DATE(func.min(getattr(model,inputName))),func.DATE(func.max(getattr(model,inputName)))).first() #TODO Dates should not be queried here, but more in the Research
        self.minValue = QDate.fromString(v[0],self.mysqlDateFormat)
        self.maxValue = QDate.fromString(v[1],self.mysqlDateFormat)
        self.initWidget()
        self.show()

    def initWidget(self):
        layout = QGridLayout(self)
        layout.setSpacing(0)

        # lbl = QLabel()
        # lbl.setText(self.inputName)
        # lbl.setContentsMargins(-10,10,10,10)

        dateDiff = math.floor((self.maxValue.year()-self.minValue.year())/2) # difference between the first date and last date, used to handle min and max values for the sliders

        minScroller = QSlider(Qt.Horizontal,self)
        minScroller.setMinimum(self.minValue.year())
        minScroller.setMaximum(self.maxValue.year())
        minScroller.setTickInterval(1)
        minScroller.setSingleStep(1)
        minScroller.setSliderPosition(self.minValue.year())

        maxScroller = QSlider(Qt.Horizontal,self)
        maxScroller.setMinimum(self.minValue.year())
        maxScroller.setMaximum(self.maxValue.year())
        maxScroller.setTickInterval(1)
        maxScroller.setSingleStep(1)
        maxScroller.setSliderPosition(self.maxValue.year())

        minEdit = QDateEdit()
        minEdit.setDate(self.minValue)
        minEdit.setDisplayFormat("yyyy")
        minEdit.setMinimumDate(self.minValue)
        minEdit.setMaximumDate(self.maxValue)

        maxEdit = QDateEdit()
        maxEdit.setDate(self.maxValue)
        maxEdit.setDisplayFormat("yyyy")
        maxEdit.setMaximumDate(self.maxValue)
        maxEdit.setMinimumDate(self.minValue)

        minScroller.valueChanged.connect(self._updateMinEdit)
        minEdit.dateChanged.connect(self._updateMinSlider)
        maxScroller.valueChanged.connect(self._updateMaxEdit)
        maxEdit.dateChanged.connect(self._updateMaxSlider)

        # layout.addWidget(lbl,0,0,0,1,QtCore.Qt.AlignCenter)

        layout.addWidget(minScroller,1,2)
        layout.addWidget(minEdit, 1, 3)

        layout.addWidget(maxScroller,2,2)
        layout.addWidget(maxEdit, 2, 3)

        self.setLayout(layout)
        self.minScroller = minScroller
        self.minEdit = minEdit
        self.maxEdit = maxEdit
        self.maxScroller = maxScroller

    def _updateMinSlider(self,date):
        self.minScroller.setSliderPosition(date.year())
        self.valueChange.emit(self.values)

    def _updateMinEdit(self, value):
        self.minEdit.setDate(QDate(value,1,1))
        self.valueChange.emit(self.values)

    def _updateMaxSlider(self,date):
        self.maxScroller.setSliderPosition(date.year())
        self.valueChange.emit(self.values)

    def _updateMaxEdit(self, value):
        self.maxEdit.setDate(QDate(value,1,1))
        self.valueChange.emit(self.values)



class AdvancedSearch(QWidget, GuiComponent):
    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.gui = parent.gui
        self.fields = ["name","runtime","genre","release","actors","directors","filename"] #TODO discover these directly with the research, for now just brutforce it
        #TODO make files and directories searchable
        self.model = Movie
        self.models = [Movie,File]
        self.data = {}
        self.search = Research()
        self.initWidget()
        self.show()
    def switchModel(self,value):
        print(value)

    def initWidget(self):
        masterLayout = QBoxLayout(QBoxLayout.TopToBottom,self)

        for model in self.models:
            #self.data[model] = {}
            layout = QFormLayout(self)
            for f in models.get_fields(model):
                if "id" in f: #we do not want users to be able to query id's (what would be the point?)
                    continue
                fieldType = models.find_type(model,f)
                lbl = QLabel()
                lbl.setText(f)
                if isinstance(fieldType, Date):
                    input = DateRangeInput(self,model,f)
                    input.valueChange.connect(lambda v, f = f, m=model: self.updateData(m,f,{"gte":v[0],"lte":v[1]}))
                    #layout.addRow(input)
                else:
                    input = QLineEdit()
                    input.setPlaceholderText(f)
                    input.textChanged.connect(lambda t, f = f, m=model : self.updateData(m,f,t))
                layout.addRow(lbl,input)
            masterLayout.addLayout(layout)
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            masterLayout.addWidget(separator)
        s = QPushButton()
        s.clicked.connect(self.query)
        s.setText("search")
        masterLayout.addWidget(s)
        self.setLayout(layout)
    def updateData(self,model,fieldName,data):
        if data is not None:
            if not model in self.data:
                self.data[model] = {}
            self.data[model][fieldName] = data
    def query(self):
        if len(self.data.keys()) < 1:
            return
        print(self.data)
        res = self.search.search(self.data)
        print(res)
        #print(list(res))
        raise Exception("Test exception")
        self.gui.dispatchAction("search-results",res)
    def handleAction(self, actionName, data):

        if actionName == "show-advanced-search":
            self.gui.dispatchAction("show-frame",self)
if __name__ == '__main__':
    from mawie.gui.Qgui import Gui
    Gui.start()