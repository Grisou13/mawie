class Event:
    name = None
    data = None

    def __init__(self, data):
        self.name = self.__class__.__name__
        self.data = data