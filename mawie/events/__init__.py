import weakref
import logging
log = logging.getLogger("mawie")

class Event:
    """Base class for emitting events
    Every event that is sent in the app must extend this base class, otherwise things might go south.
    """
    name = None
    data = None
    timeout = -1
    propogate = True
    def stopPropagate(self):
        self.propogate = False
    def setTimeout(self,time_):
        if time_ < -1:
            raise ValueError("Timeout for an event must be set to a value grater than -1")
        self.timeout = time_
    def getData(self):
        return self.data
    def setData(self,data):
        self.data = data
    def getName(self):
        return self.name
    def __init__(self, data=None):
        self.name = self.__class__.__name__
        self.data = data


class Request(Event):
    response = None
    def createResponse(self,data = None):
        self.response= Response(request=self,responseData=data)
        return self.response


class Response(Event):
    request = None
    def __init__(self, request, responseData=None):
        super(Response, self).__init__(responseData)
        self.request = request


class Start(Event):
    def __init__(self):
        pass
class Quit(Event):
    def __init__(self):
        pass

class Listener:
    """
    Helper classes that allow events to pass on from one class to another
    """

    def __init__(self, eventManager=None):
        super(Listener, self).__init__()
        if eventManager is not None and isinstance(eventManager, EventManager):
            eventManager.registerListener(eventManager)  # Automaticly register
            log.info("registering class " + self.__class__.__name__ + " in "+eventManager.__class__.__name__)
    def handle(self, event):
        if not event.propogate: #return if we were asked to explicitly not process the event
            return False


class EventManager:
    def __init__(self):
        super(EventManager, self).__init__()
        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur

    def registerListener(self, cls, extra = "default"):
        log.info("registering "+cls.__class__.__name__ + " in "+self.__class__.__name__)
        self.listeners[cls] = extra  # just register the class name

    def deleteListener(self, cls):
        del self.listeners[cls]

    def emit(self, event, on = ""):
        if not event.propogate:
            del event
            return
        elif event.timeout != -1:
            event.timeout -= 1 #add one to the timeout
        elif event.timeout == 0:
            del event
            return

        for l, extra in self.listeners.items():
            log.debug("emitting %s on listener %s [type = %s]",event,l,extra)
            if on != "" and extra != on:  # emit on a specific range of listeners
                continue
            if event.propogate != False and (event.timeout < 0 or event.timeout >= 1):
                l.handle(event)
        event.timeout -= 1



    # TODO delete the folloing methods and implement above ones
    def register_listener(self, cls):
        self.registerListener(cls)

    def delete_listener(self, cls):
        self.deleteListener(cls)




class Eventable(EventManager, Listener):
    """
    Helper class that is allowed to be at the same time an event manager, and a listener.
    This is used in the gui, since we want it to be able to handle events, and emit ones.
    It can be used in some other gui components if wanted.
    """

    def __init__(self, parent = None):
        super(Eventable, self).__init__()
        self.registerListener(self)  # this allows the ListenerClass to register ourself in the the event manager, which is ourself
