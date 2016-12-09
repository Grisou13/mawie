from . import Event


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