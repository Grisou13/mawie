import calendar
import json

import math
from PyQt5 import QtCore

from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QWidget
from sqlalchemy import Date
from sqlalchemy import distinct
from sqlalchemy import func
from datetime import date, datetime, time
from app.gui.components import GuiComponent
from app.models.Movie import Movie
from app.research.research import Research
#http://stackoverflow.com/questions/11632513/sqlalchemy-introspect-column-type-with-inheritance
def find_type(class_, colname):
    if hasattr(class_, '__table__') and colname in class_.__table__.c:
        return class_.__table__.c[colname].type
    for base in class_.__bases__:
        return find_type(base, colname)
    raise NameError(colname)

class DateRangeInput(QWidget):
    valueChange = pyqtSignal(tuple)
    @property
    def values(self):
        return self.minScroller.value(),self.maxScroller.value()
    def __init__(self,parent = None, inputName = None,*arg,**kwargs):
        super().__init__(parent,*arg,**kwargs)
        if inputName is None : pass
        self.inputName = inputName
        self.data = {}
        #TODO Dates should not be queried here, but more in the Research
        v = Movie.query(func.DATE(func.min(getattr(Movie,inputName))),func.DATE(func.max(getattr(Movie,inputName)))).first()
        format = 'yyyy-MM-dd'
        self.minValue = QDate.fromString(v[0],format)
        self.maxValue = QDate.fromString(v[1],format)
        self.initWidget()
        self.show()

    def initWidget(self):
        layout = QGridLayout(self)
        layout.setSpacing(0)

        lbl = QLabel()
        lbl.setText(self.inputName)

        dateDiff = math.floor((self.maxValue.year()-self.minValue.year())/2) # difference between the first date and last date, used to handle min and max values for the sliders

        minScroller = QSlider(Qt.Horizontal,self)
        minScroller.setMinimum(self.minValue.year())
        minScroller.setMaximum(self.maxValue.year())
        minScroller.setTickInterval(1)
        minScroller.setSingleStep(1)
        minScroller.setPageStep(1)
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
        minEdit.setMaximumDate(self.minValue)

        maxEdit = QDateEdit()
        maxEdit.setDate(self.maxValue)
        maxEdit.setDisplayFormat("yyyy")
        maxEdit.setMaximumDate(self.maxValue)
        maxEdit.setMinimumDate(self.minValue)

        minScroller.valueChanged.connect(self._updateMinYear)
        minEdit.dateChanged.connect(self._updateMinSlider)
        maxScroller.valueChanged.connect(self._updateMaxYear)
        maxEdit.dateChanged.connect(self._updateMaxSlider)

        layout.addWidget(lbl,0,0,0,1,QtCore.Qt.AlignLeft)

        layout.addWidget(minScroller,1,1)
        layout.addWidget(minEdit, 1, 2)

        layout.addWidget(maxScroller,2,1)
        layout.addWidget(maxEdit, 2, 2)

        self.setLayout(layout)
        self.minEdit = minEdit
        self.maxEdit = maxEdit
        self.minScroller = minScroller
        self.maxScroller = maxScroller

    def _updateMaxSlider(self,date):
        self.maxScroller.setSliderPosition(date.year())
        self.valueChange.emit(self.values)
    def _updateMinSlider(self,date):
        self.minScroller.setSliderPosition(date.year())
        self.valueChange.emit(self.values)
    def _updateMaxYear(self,value):
        print("max " + str(self.maxScroller.value()))
        print("min " + str(self.minScroller.value()))
        if self.maxScroller.value() <= self.minScroller.value():
            print("max scroller smaller than min scroller")
            self.maxScroller.setSliderPosition(value)
            #self.maxScroller.setMinimum(self.minScroller.value())
        self.maxEdit.setDate(QDate(value,1,1))
        self.valueChange.emit(self.values)
    def _updateMinYear(self,value):
        print("max " + str(self.maxScroller.value()))
        print("min " + str(self.minScroller.value()))
        if self.maxScroller.value() < self.minScroller.value():
            print("min bigger than max")
            #self.minScroller.setMaximum(self.maxScroller.value())
        self.minEdit.setDate(QDate(self.minScroller.value(),1,1))
        self.valueChange.emit(self.values)

class AdvancedSearch(QWidget, GuiComponent):
    def __init__(self, parent = None, gui = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        parent.addWidget(self)
        gui.register_listener(self)
        self.gui = gui
        self.fields = ["name","runtime","genre","release","actors","directors","filename"] #TODO discover these directly with the research, for now just brutforce it
        self.model = Movie
        self.data = {}
        self.search = Research()
        self.initWidget()
        self.show()
    def initWidget(self):
        print("init wodget")
        layout = QFormLayout(self)
        for f in self.fields:
            if not f in self.search.get_fields(self.model):
                continue
            fieldType = find_type(self.model,f)
            self.data[f] = None
            if isinstance(fieldType, Date):
                input = DateRangeInput(self,f)
                input.valueChange.connect(lambda v, f = f: self.updateData(f,v))
                print(f)
                layout.addRow(input)
            else:
                lbl = QLabel()
                lbl.setText(f)
                input = QLineEdit()

                input.setPlaceholderText(f)
                input.textChanged.connect(lambda t, f = f : self.updateData(f,t))
                layout.addRow(lbl,input)

        s = QPushButton()
        s.clicked.connect(self.query)
        s.setText("search")
        layout.addRow(s)
        self.setLayout(layout)
    def updateData(self,fieldName,data):
        if isinstance(data,tuple) or isinstance(data,list) or isinstance(data,set):
            self.data[fieldName] = {"in":data}
        else:
            self.data[fieldName] = data
    def query(self):
        res = self.search.search({self.model:dict(self.data)})
        self.gui.dispatchAction("search-results",res)
if __name__ == '__main__':
    from app.gui.Qgui import Gui
    Gui.start()