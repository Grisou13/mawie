import os
import sys
from exceptions import *
if __name__ == '__main__':
    sys.path.append(os.path.join(os.getcwd(), "../../"))
import PTN
import json
import re

from app.models.File import File
#import app.models.Movie

class Explorer():
    #database connector uses SQLAlchemy
    movieFileMovie = object()

    def __init__(self, path, databaseName=".cache/main.sqlite"):

        if (path is None) or os.path.exists(path) is False:
            raise IsADirectoryError("Film directory not found")

        if (self.checkDirIfEmpty(path)):
            raise FileNotFoundError("No file has been found in the {} path".format(path))

        self.path = path
        self.movieFileConnector = File

        # r = self.movieModel.query()
        # print(r)

    def checkDirIfEmpty(self, dir):
        """ Check for file in folder and subfolder (only 1 folder of depth) """
        #TODO need to be tested in a folder with files ONLY in subfolder
        f = True
        for dirpath, dirnames, files in os.walk(dir):
            if files:
                #Found
                f = False
            if not files:
                #Not found but....
                if dirnames:
                    for dpath, dnames, fls in os.walk(dirpath):
                        if fls:
                            #Found in subfolde ! :)
                            f = False
        return f

    def getFolderContent(self, path=None):
        if path is None:
            path = self.path

        assert os.path.exists(path)
        return os.listdir(path)

    def nameParsing(self, movieList):
        #TODO in folder, return the files in it and not the folder !
        if not (isinstance(movieList, list)):
            raise TypeError("Expecting a list")
        cleanMovieList = {}
        for dirtyMovie in movieList:
            #TODO optimise REGEX parsing (PTN/patterns.py)
            parsed = PTN.parse(dirtyMovie.replace(".", " "))
            cleanMovieList[parsed['title']] = parsed
        return cleanMovieList

    def addMoviesToDatabase(self, movieList):
        assert isinstance(movieList, dict)
        #TODO add the path of te movie :)))))
        #WITH NORMAL SLASH
        for movie, data in movieList.items():
            # useless data from the parser
            if("episodeName" in data):
                del data["episodeName"]
            if("proper" in data):
                del data["proper"]
            """try:
                k = data["title"]
            except (IndexError, KeyError):
                print(data)
                sys.exit("decomment that ")"""
            # replace any list in the data by an arrray (['FRENCH', 'BDRip'] => 'FRENCH, BDRip')
            for k,v in data.items():
                if(isinstance(v, list)):
                    # yeah i know, python is weird sometimes
                    data[k] = ", ".join(v)
                elif(not isinstance(v, str) and not isinstance(v, int)):
                    raise TypeError("Movie data format not conform")
            #print data if you want to know why i used the **kwargs
            
            moveFile = self.movieFileConnector(**data).save()


    def getAllMoviesFromDatabase(self):
        return self.movieFileConnector.query()

    def writeContentInJson(self, data, file="data.json"):
        with open(file,"w+") as outfile:
            json.dump(data, outfile)

if __name__ == '__main__':
    # get stuff done
    explorer = Explorer("../../stubs/FILM_a_trier")
    lst = explorer.nameParsing(explorer.getFolderContent())

    #explorer.addMoviesToDatabase(lst)
    sys.exit("end of normal execution")
    fromdb = explorer.getAllMoviesFromDatabase()
    for movie in fromdb:
        print(movie.path)

        """
        if(movie.title is None):
            print(movie.updated_at)
            print([attribute for attribute in dir(movie) if attribute[0].islower()])
        print(movie.updated_at)"""
    sys.exit("OUIIII")

"""
    movie data structure :
    "MovieName": {
        "excess": "TRUEFRENCH",
        "title": "Les 101 Dalmatiens 2",
        "year": 2009,
        "quality": "DVDRip",
        "codec": "Xvid",
        "group": "Ac3-UTT avi",
        "audio": "AC3"
    },

"""
