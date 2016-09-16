from sqlalchemy import Column

from app.models.Movie import Movie
from app.models import db
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
            for mov in m.query().filter(m.name.like("%"+query+"%"),m.desc.like("%"+query+"%")):
                yield mov
        else:
            if isinstance(filters,list):
                for f in filters:
                    yield self.filter(f,query)
            else:
                yield self.filter(filters,query)
        # query local db
        # query remote db
        pass
    def getFields(self,cls):
        _ = {}
        for col in cls.__table__.columns:
            name = str(col).split(".")[1]
            _[name.lower()] = name
        return _
    def filter(self,f,query):
        _f = self.getFields(self.model)
        print(_f)
        if f.lower() in _f.keys():
            return list(self.model.query().filter(getattr(self.model, str(_f[f.lower()])).like("%" + query + "%")))
        else:
            raise RuntimeError("Well the filter doesnt exist you know?")
    async def localSearch(self):
        pass
    async def remoteSearch(self):
        pass

if __name__ == '__main__':
    r = Research()
    print(r.search("Sayo Saruta","Actors").__next__())
