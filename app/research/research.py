from sqlalchemy import Column

from app.models.Movie import Movie
from app.models import db

from sqlalchemy import or_

class FilterDoesntExist(Exception):pass

class Searchable(object):
    """ Prototype for any searchable item """

    def __init__(self, cls):
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
    default_cols = ["name","desc"]
    # only implement local research for films
    def search(self, query, filters=None,):
        """ :return generator"""
        m = self.model
        cols = self.default_cols
        if isinstance(filters, list):
            cols.append(filters)
        elif isinstance(filters,str):
            new_cols = filters.replace(';',' ').replace(',',' ').replace(':',' ').split()
            cols = list(set(cols + [x.lower() for x in new_cols]))
        if len(cols) <=0:
            return iter([])
        q = self.queryModelOnColumn(*cols, query)
        return iter(q.all())

        # query local db
        # query remote db
        pass

    @staticmethod
    def getFields(cls):
        _ = []
        for col in cls.__table__.columns:
            name = str(col).split(".")[1]
            _.append(name)
        return _

    def queryModelOnColumn(self, *args, **kwargs):
        """
        Querys the searchable model on specified columns.
        Columns are either specified by arg list, and last element is used as the query : queryModelOnColumn("col1","col2","query"
        Wither by arguments queryModelOnColumn(query="some thing to search",columns=["a","list","of","cols"])
        Or seperated list of columns by [;,:] queryModelOnColumn(query="some thing to search",columns="a,list,of,cols")
        Idea came from http://stackoverflow.com/a/28270753
        Needs some optimization for complexity
        :param args:
        :param kwargs:
        :return:
        """
        if "query" in kwargs:
            if "columns" in kwargs and isinstance(list,kwargs["columns"]):
                return self.model.query().filter(
                    or_(*[getattr(self.model, name).like("%" + str(kwargs["query"]) + "%") for name in kwargs["columns"]]))
            elif "columns" in kwargs and isinstance(str, kwargs["columns"]):
                cols = kwargs["columns"].replace(';',' ').replace(',',' ').replace(':',' ').split()
                return self.model.query().filter(
                    or_(*[getattr(self.model, name).like("%" + str(kwargs["query"]) + "%") for name in
                          cols]))

        fields = list(args)[:-1]
        authorized_fields = self.getFields(self.model)
        return self.model.query().filter(or_(*[ getattr(self.model, name).like("%"+str(args[-1])+"%") for name in fields if name in authorized_fields ]))



if __name__ == '__main__':
    r = Research()
    searchable = r.search("Isabelle","actor")
    print(searchable)
    for s in searchable:
        print(s)
