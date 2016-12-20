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


class FileParsedResponse(Response):
    pass


class ParsingEnded(Event):
    pass


class ParsingStarted(Event):
    pass


class GoogleItSearchRequest(Request):
    pass


class GoogleItResponse(Response):
    pass


class GoogleItInternalRequest(Event):
    """
    Data represents the number of tries the google it tried to get the movie, and the movie title
    :param tries: Number of tries the google it already did
    :type tries: int
    :param url: Url to try:
    :type url: str
    :param title: Title of the searching movie
    :type title: str

    """
    def __init__(self, tries, url, title):
        self.url = url
        self.tries = tries
        self.title = title


class GoogleItResult(Event):
    pass

class TryLink(Event):
    """
    Used when trying an imdb (or any other source) link. This allows us to fetch the title
    """
    def __init__(self,url,expectedTitle):
        self.url = url
        self.expectedTitle = expectedTitle


class TryLinkResult(Event):
    def __init__(self, expectedTitle, data):
        self.expected = expectedTitle
        self.data = data


class ExplorerParsingRequest(Request):
    pass


class ExplorerParsingResponse(Response):
    pass
