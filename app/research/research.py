
import os
if __name__ == '__main__':
    import sys
    sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__),"../","../")))
from sqlalchemy import or_

from app.models import db
from app.models.Movie import Movie
from sqlalchemy_elasticquery import elastic_query

class FilterDoesNotExist(Exception):pass
class FieldDoesNotExist(Exception):pass
class NotAModel(Exception): pass
import types

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
    def __init__(self, col):
        self.column = col

class FilterableList:
    filters = []


class Research:
    """ main research class """
    default_cols = ["name"]
    default_model = Movie
    def __init__(self,*args,**kwargs):
        self.model = self.default_model
        self.cols = self.default_cols
        if "model" in kwargs:
            self.model = kwargs["model"]
            self.cols = []
            del kwargs["model"]
        if "cols" in kwargs:
            self.cols = kwargs["cols"]
            del kwargs["cols"]

    def _aggregate_results(self):
        pass

    def _to_filters(self, model, st):
        pass
    def setModel(self,m):
        self.model = m
        self.cols = [] # no more defaul cols when reassigning the model
    # only implement local research for films
    def search(self, query = "", filters=None):
        """ :return generator"""
        m = self.model
        cols = self.cols
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
        if isinstance(query, dict):
            q = self.queryModelOnMultipleColumns(query)
        else:
            q = self.queryModelOnColumn(*cols, query, m)
        if isinstance(q,list):
            for i in q:
                yield i
        elif isinstance(q, types.GeneratorType):
            yield q
        else:
            for res in q.yield_per(5):
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
    def queryModelOnMultipleColumns(self,*args,**kwargs):
        """
        Queries a model with one/mutliple queries per column (SELECT * FROM ... WHERE col = query1, col = query2, col2 = query3, col3 = query4)

        The same thing for queryModelOnColumn, the query can be either a list or string (seperated with ;,:)
        :param args:
        :param kwargs:
        :return:
        """
        print("asd")
        queries = kwargs["queries"] if "queries" in kwargs else args[0]
        # fields = queries.keys()
        # authorized_fields = self.get_fields(model)
        # if set(fields).issubset(set(authorized_fields)):
        for model, filters in queries.items():
            print("ad")
            res = elastic_query(model, filters)
            print(res)
            for i in res.yield_per(5):
                yield i
        # else:
        #     raise FieldDoesNotExist("Field " + str(fields) + " does not exist in model " + str(authorized_fields))


    def queryModelOnColumn(self, *args, **kwargs):
        """
        Query's the searchable model with one query string on number of columns. (SELECT * FROM .. WHERE col = query, col2 = query, col3 = query)

        Columns are either specified by arg list, and last element is used as the query : queryModelOnColumn("col1","col2","query",modelInstance)
        Wither by arguments queryModelOnColumn(query="some thing to search",columns=["a","list","of","cols"],model=modelInstance)
        Or separated list of columns by [;,:] queryModelOnColumn(query="some thing to search",columns="a,list,of,cols",model=modelInstance)
        And the last argument is the model
        Idea came from http://stackoverflow.com/a/28270753
        Needs some optimization for complexity

        :param args:
        :param kwargs:
        :kwargs
            - columns The columns on which the model will be queried
            - model The model to query, by default the search will take the default_model (see Research.__init__)
            - query The query string on which all the columns will be compared to
        :return: SqlAlchemyQuery
        """
        model = kwargs["model"] if "model" in kwargs else args[-1]
        query = kwargs["query"] if "query" in kwargs else args[-2]
        fields = kwargs["columns"] if "columns" in kwargs else list(args)[:-2]
        if isinstance(fields, str):
            fields = fields.replace(';', ' ').replace(',', ' ').replace(':', ' ').split()
        authorized_fields = self.get_fields(model)
        # try:
        #     authorized_fields = self.get_fields(model)
        # except NotAModel:
        #     authorized_fields = self.get_fields(self.default_model) #query on the default model so functionality is not altered

        if set(fields).issubset(set(authorized_fields)): #small hack with sets, python cannot compare list (http://stackoverflow.com/questions/3931541/python-check-if-all-of-the-following-items-is-in-a-list)
            return model.query().filter(or_(*[getattr(model, name).like("%" + str(query) + "%") for name in fields]))
        else:
            raise FieldDoesNotExist("Field " + str(fields) + " does not exist in model " + str(authorized_fields))

    def setCols(self, param):
        self.cols = param


if __name__ == '__main__':
    r = Research()
    searchable = r.search("The g")
    print(searchable)
    print(list(r.search({Movie:{"title":"The"}})))
