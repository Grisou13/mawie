import os
import PTN
import json
import sys
import sqlite3

class Explorer():

    path = ""
    # It uses SQLAlchemy
    databaseConnector = object()

    def __init__(self, path, databaseName="mawieDatabse"):
        #print(path)
        if (path is None) and os.path.exists(path) is True:
            raise IsADirectoryError("Directory not found")
        else:
            self.path = path

        self.databaseConnector = databaseConnector(databaseName)

    def getFolderContent(self):
        return os.listdir(self.path)

    def nameParsing(self, movieList):
        if not (isinstance(movieList, list)):
            raise TypeError("Expecting a list")
        cleanMovieList = {}
        for dirtyMovie in movieList:

            parsed = PTN.parse(dirtyMovie.replace(".", " "))
            #cleanMovieList[parsed['title']] = dirtyMovie
            if "rouge" in parsed['title'].lower():
                print(parsed)

            cleanMovieList[parsed['title']] = parsed
            #print(dirtyMovie)
            #print(PTN.parse(dirtyMovie))
            #print(type(cleanMovieList))
            #cleanMovieList.add(PTN.parse(dirtyMovie))
        return cleanMovieList

    def writeContentInJson(self, data, file="data.json"):
        with open(file,"w+") as outfile:
            json.dump(data, outfile)
