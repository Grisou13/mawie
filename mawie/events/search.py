from . import Event, Response, Request


class GotSearchResults(Event):
    pass


class SearchResult(Event):
    pass


class SearchRequest(Request):
    pass

class SearchResponse(Response):
    pass