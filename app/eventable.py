"""
Helper classes that allow events to pass on from one class to another
"""
import weakref


class Eventable():
    def __init__(self):
        self.listeners = weakref.WeakKeyDictionary()  # we don't care about keys, and this might contain more references than 2 components in the futur
    def register_listener(self, cls):
        self.listeners[cls] = 1

    def dispatchAction(self, actionName, actionData = None):
        print("dispatching action : "+actionName )
        for l in self.listeners.keys():
            l.handleAction(actionName, actionData)
    def requestAction(self, originClass, actionName):
        for l in self.listeners.keys():
            if isinstance(l, originClass): continue  # we don't request on the same object... would be pointless
            originClass.handleAction("request_" + actionName, l.requestAction(actionName))