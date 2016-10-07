from sqlalchemy import or_

from app.models.Movie import Movie

class FilterDoesNotExist(Exception):pass
class FieldDoesNotExist(Exception):pass

class SearchableItem:
    def __init__(self, model, defaultColumn):
        """

        :param model:
        :param defaultColumn:
        :type model: ActiveAlchemy.Model
        """
        self._raw = model
    def __str__(self):
        return self._raw
    def __getattr__(self, item):
        return self._raw.__getattr__(item)

class Research:
    model = Movie
    """ main research class """
    default_cols = ["name","desc"]
    # only implement local research for films
    def search(self, query, filters=None):
        """ :return generator"""
        m = self.model
        cols = self.default_cols
        if isinstance(filters, list):
            #either append cols or just assign cols to filter
            #cols.append(filters)
            cols = filters
        elif isinstance(filters,str):
            new_cols = filters.replace(';',' ').replace(',',' ').replace(':',' ').split()
            #cols = list(set(cols + [x.lower() for x in new_cols]))
            cols = [x.lower() for x in new_cols]
        if len(cols) <=0:
            yield [] #return an empty iterator
        q = self.queryModelOnColumn(*cols, query)
        for res in q.all():
            yield res

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
        :return: Generator of app.models.Movie.Movie
        """
        if "query" in kwargs:
            if "columns" in kwargs and isinstance(list,kwargs["columns"]):
                return self.model.query().filter(
                    or_(*[getattr(self.model, name).like(str(kwargs["query"])) for name in kwargs["columns"]]))
            elif "columns" in kwargs and isinstance(str, kwargs["columns"]):
                cols = kwargs["columns"].replace(';',' ').replace(',',' ').replace(':',' ').split()
                return self.model.query().filter(
                    or_(*[getattr(self.model, name).like(str(kwargs["query"])) for name in
                          cols]))

        fields = list(args)[:-1]
        authorized_fields = self.getFields(self.model)
        if set(fields).issubset(set(authorized_fields)): #small hack with sets, python cannot compare list (http://stackoverflow.com/questions/3931541/python-check-if-all-of-the-following-items-is-in-a-list)
            return self.model.query().filter(or_(*[ getattr(self.model, name).like("%"+str(args[-1])+"%") for name in fields ]))
        raise FieldDoesNotExist("Field " + str(fields) + " does not exist in model " + str(authorized_fields))
if __name__ == '__main__':
    r = Research()
    searchable = r.search("WWE")
    print(searchable)
    for s in searchable:
        print(s.files)
