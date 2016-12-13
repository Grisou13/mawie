from . import Event, Request


class SearchStarted(Event):
    pass


class MovieParsed(Event):
    pass


class MovieNotParsed(Event):
    pass


class ParseDirectoryRequest(Request):
    pass


class FileParsed(Event):
    pass


class FileNotParsed(Event):
    pass


class ParsingEnded(Event):
    pass


class ParsingStarted(Event):
    pass