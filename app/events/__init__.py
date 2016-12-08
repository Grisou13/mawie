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


class Eventable(object):
    def __init__(self):
        super(Eventable,self).__init__()
        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur
    def register_listener(self, cls):
        self.listeners[cls] = cls.__class__.__name__ #just register the class name
    def delete_listener(self,cls):
        del self.listeners[cls]
    def emit(self, event):
        for l in self.listeners.keys():
            l.handleAction(event)
    def dispatchAction(self, actionName, actionData = None):
        print("dispatching action : "+actionName )
        for l in self.listeners.keys():
            l.handleAction(actionName, actionData)
    def requestAction(self, originClass, actionName):
        for l in self.listeners.keys():
            if isinstance(l, originClass): continue  # we don't request on the same object... would be pointless
            originClass.handleAction("request_" + actionName, l.requestAction(actionName))