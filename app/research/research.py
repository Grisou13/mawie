
from sqlalchemy import or_

from app.models import db
from app.models.Movie import Movie

class FilterDoesNotExist(Exception):pass
class FieldDoesNotExist(Exception):pass
class NotAModel(Exception): pass


class SearchableItem:
    def __init__(self, model, defaultColumn):
        """

        :param model:
        :param defaultColumn:
        :type model: ActiveAlchemy.Model
        :type defaultColumn: str
        """
        self._raw = model
    def __str__(self):
        return self._raw
    def __getattr__(self, item):
        return self._raw.__getattr__(item)


class Filterable:
    column = "column_on_model"
    model = "model_name"


class FilterableList:
    filters = []


class Research:
    """ main research class """
    default_cols = ["name"]
    default_model = Movie

    def _aggregate_results(self):
        pass

    def _to_filters(self, model, st):
        pass

    # only implement local research for films
    def search(self, query, filters=None):
        """ :return generator"""
        m = self.default_model
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
        q = self.queryModelOnColumn(*cols, query, m)
        for res in q.all():
            print(res)
            yield res

    @staticmethod
    def get_fields(cls):
        if not hasattr(cls,'__table__'):
            raise NotAModel("The class "+str(cls)+" is not an instance of a ActiveAlchemy model")
        _ = []
        for col in cls.__table__.columns:
            name = str(col).split(".")[1]
            _.append(name)
        return _

    def queryModelOnColumn(self, *args, **kwargs):
        """
        Query's the searchable model on specified columns.

        Columns are either specified by arg list, and last element is used as the query : queryModelOnColumn("col1","col2","query"
        Wither by arguments queryModelOnColumn(query="some thing to search",columns=["a","list","of","cols"])
        Or separated list of columns by [;,:] queryModelOnColumn(query="some thing to search",columns="a,list,of,cols")
        And the last argument is the model
        Idea came from http://stackoverflow.com/a/28270753
        Needs some optimization for complexity

        :param args:
        :param kwargs:
        :return: Rows of all data for 1 model
        """
        model = kwargs["model"] if "model" in kwargs else args[-1]
        query = kwargs["query"] if "query" in kwargs else args[-2]
        fields = kwargs["columns"] if "columns" in kwargs else list(args)[:-2]
        if isinstance(fields, str):
            fields = fields.replace(';', ' ').replace(',', ' ').replace(':', ' ').split()
        try:
            authorized_fields = self.get_fields(model)
        except NotAModel:
            authorized_fields = self.get_fields(self.default_model) #query on the default model so functionality is not altered

        if set(fields).issubset(set(authorized_fields)): #small hack with sets, python cannot compare list (http://stackoverflow.com/questions/3931541/python-check-if-all-of-the-following-items-is-in-a-list)
            return model.query().filter(or_(*[getattr(model, name).like("%" + str(query) + "%") for name in fields]))
        raise FieldDoesNotExist("Field " + str(fields) + " does not exist in model " + str(authorized_fields))
if __name__ == '__main__':
    r = Research()
    searchable = r.search("")
    print(searchable)
    for s in searchable:
        print(s)
