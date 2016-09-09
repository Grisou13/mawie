
class Searchable(object):
    """ Prototype for any searchable item """

    def __init__(self,cls):
        pass

    def search(self, query):
        for f in self.__dict__:
            pass

    def applyFilter(self, filter):
        pass


class SearchableItem:
    pass


class Research:
    model = Movie
    """ main research class """
    #only implement local research for films
    def search(self, query, type, filters=None):

        # query local db
        # query remote db
        pass

    async def localSearch(self):
        pass
    async def remoteSearch(self):
        pass

if __name__ == '__main__':
    from app.models.Movie import Movie

    r = Research()
    r.search("harry potter", Searchable(Movie))
