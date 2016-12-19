import traceback

from . import Event

class ShowAdvancedSearchFrame(Event):
    pass

class ShowFrame(Event):
    pass
    # def __init__(self,frame, data = None):
    #     self.frame = frame
    #     self.data = data



class SearchResults(Event):
    pass


class ErrorEvent(Event):
    type = None
    value = None
    _traceback = None
    @property
    def traceback(self):
        return self._traceback
    @traceback.setter
    def traceback(self,val):
        if isinstance(val,str):
            self._traceback = val
        else:
            self._traceback = traceback.format_tb(val)
    def __init__(self,type_,value,traceback):
        super(ErrorEvent,self).__init__()
        self.type = type_
        self.value = value
        self.traceback = traceback


class ShowMovieList(Event):
    pass

class ShowExplorer(Event):
    pass

class ShowSettings(Event):
    pass

class ShowMovieInfo(Event):
    pass

class ShowAdvancedSearch(Event):
    pass
