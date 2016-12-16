from . import Event, Request, Response


class SearchStarted(Event):
    pass


class MovieParsed(Event):
    pass


class MovieNotParsed(Event):
    pass


class ParsingEnded(Event):
    pass


class ParsingStarted(Event):
    pass


class GoogleItEvent(Request):
    pass


class GoogleItResponse(Response):
    pass
