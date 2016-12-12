from . import Event


class ShowFrame(Event):
    pass


class ErrorEvent(Event):
    type = None
    value = None
    traceback = None
    def __init__(self,type_,value,traceback):
        super(ErrorEvent,self).__init__()
        self.type = type_
        self.value = value
        self.traceback = traceback