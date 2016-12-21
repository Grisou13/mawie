#create database and tables if they don't exist

from .File import File
from .Movie import Movie
from .db import db
db.create_all()


class NotAModel(Exception): pass
not_authorized_fields = ["is_deleted","created_at","updated_at","deleted_at"]
def get_fields(cls):
    if not hasattr(cls,'__table__'):
        raise NotAModel("The class "+str(cls)+" is not an instance of a ActiveAlchemy model")
    _ = []
    for col in cls.__table__.columns:
        name = str(col).split(".")[1]
        if name not in not_authorized_fields:
            _.append(name)
    return _

#http://stackoverflow.com/questions/11632513/sqlalchemy-introspect-column-type-with-inheritance
def find_type(class_, colname):
    if hasattr(class_, '__table__') and colname in class_.__table__.c:
        return class_.__table__.c[colname].type
    for base in class_.__bases__:
        return find_type(base, colname)
    raise NameError(colname)