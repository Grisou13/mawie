from . import Event

class Tick(Event):
    """
    Every time the background app ticks, this event is dispatched.
    data contains the time at which the event was dispatched
    """
    pass


class MoveToForeground(Event):
    pass