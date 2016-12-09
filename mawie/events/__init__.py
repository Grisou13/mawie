class Event:
    name = None
    data = None

    def __init__(self, data):
        self.name = self.__class__.__name__
        self.data = data


"""
Helper classes that allow events to pass on from one class to another
"""
import weakref


class Listener(object):
    def __init__(self, eventManager=None):
        super(Listener, self).__init__()
        if eventManager is not None:
            eventManager.registerListener(self)  # Automaticly register

    def handle(self, event):
        pass


class EventManager(object):
    def __init__(self):
        super(EventManager, self).__init__()
        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur


    def registerListener(self, cls):
        self.listeners[cls] = cls.__class__.__name__  # just register the class name

    def deleteListener(self, cls):
        del self.listeners[cls]

    def emit(self, event):
        for l in self.listeners.keys():
            l.handle(event)

    # TODO delete the folloing methods and implement above ones
    def register_listener(self,cls):
        self.registerListener(cls)
    def delete_listener(self,cls):
        self.deleteListener(cls)
    def dispatchAction(self, actionName, actionData=None):
        print("dispatching action : " + actionName)
        for l in self.listeners.keys():
            l.handleAction(actionName, actionData)

    def requestAction(self, originClass, actionName):
        for l in self.listeners.keys():
            if isinstance(l, originClass): continue  # we don't request on the same object... would be pointless
            originClass.handleAction("request_" + actionName, l.requestAction(actionName))


class Eventable(EventManager, Listener):
    """
    Helper class that is allowed to be at the same time an event manager, and a listener.
    This is used in the gui, since we want it to be able to handle events, and emit ones.
    It can be used in some other gui components if wanted.
    """

    def __init__(self):
        super(Eventable, self).__init__()  # this allows the ListenerClass to register ourself in the the event manager, which is ourself
