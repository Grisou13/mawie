class NotImplemented(Exception): pass


class GuiComponent(object):
    def requestAction(self, actionName):
        raise NotImplemented("You need to implement the method requestControllerAction in your gui component object")

    def handleAction(self, actionName, data):
        raise NotImplemented("You need to implement the method handleControllerAction in your gui component object")

