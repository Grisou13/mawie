import math
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QWidget
from sqlalchemy import func


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
