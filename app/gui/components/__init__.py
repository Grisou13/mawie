class NotImplemented(Exception): pass


class GuiComponent(object):
    def __init__(self):
        pass
    def requestAction(self, actionName):
        raise NotImplemented("You need to implement the method requestAction in your gui component object")

    def handleAction(self, actionName, data):
        raise NotImplemented("You need to implement the method handleAction in your gui component object")
