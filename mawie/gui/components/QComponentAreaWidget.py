import logging

from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QStackedWidget

from mawie.events.gui import ShowFrame
from mawie.gui.components.QAdvancedSearchWidget import AdvancedSearch
from mawie.gui.components.QExplorerWidget import ExplorerWidget
from mawie.gui.components.QMovieListWidget import MovieListWidget
from mawie.gui.components.QMovieWidget import MovieWidget
from mawie.gui.components.QSettings import SettingsWidget
from mawie.models.Movie import Movie

log = logging.getLogger("mawie")
'''
ComponentArea is a QStackedWidget which


'''
class ComponentArea(QStackedWidget):
    def __init__(self, gui ,parent=None):
        super().__init__(parent)
        self.gui = gui

        self.widgetStore = {}
        self.currentChanged.connect(self.onCurrentChange)
        self.initWidget()

    def addWidget(self,widget):
        widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        widget.show()
        self.gui.registerListener(widget)
        super(ComponentArea, self).addWidget(widget)

    def onCurrentChange(self,index):
        w = self.widget(index)
        w.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        #self.adjustSize()
        #w.adjustSize()
        w.show()

    def addWidget(self,widget):
        """
        this method overrides method from QStackedWidget. it just registers the widget as listener of event
        :param widget: QWidget
        """
        log.info("adding widget %s",widget.__class__.__name__)
        if widget.__class__.__name__ not in self.widgetStore:
            widget.gui = self.gui
            widget.emit = lambda e: self.gui.emit(e)
            self.gui.registerListener(widget)
            self.widgetStore[widget.__class__.__name__] = widget
            #self.gui.register_listener(widget)
            super(ComponentArea,self).addWidget(widget)

    def initWidget(self):

        self.addWidget(AdvancedSearch(self))
        self.addWidget(MovieWidget(self))
        self.addWidget(SettingsWidget(self))
        s = MovieListWidget(self)
        self.addWidget(s)
        self.addWidget(AdvancedSearch(self))
        self.addWidget(ExplorerWidget(self))
        self.setCurrentWidget(s)
        # if there are movies we display the MovieListWidget otherwise we display the Explorer
        if Movie.query().count() >0:
            self.setCurrentWidget(s)
        else:
            self.setCurrentWidget(self.widgetStore[ExplorerWidget.__name__])
        log.info("initialized : %s widgets",self.widgetStore)

    def handle(self,event):
        #super().handle(event)
        # Display the widget when a ShowFrame event is handled
        if isinstance(event, ShowFrame):
            if event.frame.__class__.__name__ in self.widgetStore:
                event.stopPropagate()
                event.timeout = 0
                self.setCurrentWidget(self.widgetStore[event.frame.__class__.__name__ ])

if __name__ == '__main__':
    from mawie.gui import start
    start()