import os
import PTN
import json
import sys
#sql and shit
from sqlalchemy.orm import
from sqlalchemy import create_engine

from app.explorer.explorer import *

class Explorer():

    path = ""
    #database connector uses SQLAlchemy
    databaseConnector = object()

    def __init__(self, path, databaseName=".cache/main.sqlite"):
        if (path is None) and os.path.exists(path) is True:
            raise IsADirectoryError("Directory not found")
        self.path = path
        def initiateConnector():
            try:
                engine = create_engine(H.DB_PATH)
                base.Base.metadata.create_all(engine, checkfirst=True)
                #serve as a factory for new session objects
                Session = sessionmaker(bind=engine)
                #bound the db
                return Session()
                #use the fellow example
                #>>> ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
                #>>> session.add(ed_user)
            except ValueError as e:
                print(e)

        self.connector = initiateConnector()


    def getFolderContent(self, path=None):
        if path is None:
            path = self.path
        assert os.path.exists(path)
        return os.listdir(path)

    def nameParsing(self, movieList):
        if not (isinstance(movieList, list)):
            raise TypeError("Expecting a list")
        cleanMovieList = {}
        for dirtyMovie in movieList:
            #todo optimise REGEX parsing (PTN/patterns.py)
            parsed = PTN.parse(dirtyMovie.replace(".", " "))
            #cleanMovieList[parsed['title']] = dirtyMovie

            print(type(cleanMovieList))
            #print(dirtyMovie)
            #print(PTN.parse(dirtyMovie))
            #print(type(cleanMovieList))
            #cleanMovieList.add(PTN.parse(dirtyMovie))
        return cleanMovieList

    def addMoviesToDatabase(self, movieList):
        assert isinstance(movieList, list)
        self.session.add(movieList)

    def writeContentInJson(self, data, file="data.json"):
        with open(file,"w+") as outfile:
            json.dump(data, outfile)

if __name__ == '__main__':
    #do stuff
    explorer = Explorer("../../stubs/FILM_a_trier")
    explorer.writeContentInJson(explorer.nameParsing(explorer.getFolderContent()))
    print("stuff is done")
