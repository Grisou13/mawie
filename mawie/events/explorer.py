from . import Event, Request, Response


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


class GoogleItSearchRequest(Request):
    pass


class GoogleItResponse(Response):
    pass

class GoogleItResult(Event):
    pass

class ExplorerParsingRequest(Request):
    pass


class ExplorerParsingResponse(Response):
    pass
