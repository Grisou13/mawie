from app.models.Movie import Movie
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
    def search(self, query, filters=None):

        m = self.model
        if filters is None:
            return m.query().filter(m.name.like("%"+query+"%"),m.desc.like("%"+query+"%"))
        else:
            if filter in m.columns():
                return m.query.filter(m.columns())
            else:
                raise RuntimeError("Well the filter doesnt exist you know?")
        # query local db
        # query remote db
        pass

    async def localSearch(self):
        pass
    async def remoteSearch(self):
        pass

if __name__ == '__main__':
    r = Research()
    r.search("The")
