import os
import sys
from exceptions import *
if __name__ == '__main__':
    sys.path.append(os.path.join(os.getcwd(), "../../"))
import PTN
import json
# import sys
#sql and shit


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
        self.movieFileMovie = File()
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

        for movie, data in movieList.items():
            #what im trying here is fucked up
            #credits to http://stackoverflow.com/questions/2553354/how-to-get-a-variable-name-as-a-string-in-python
            print(movie, data)

            sys.exit()

    def getAllMoviesFromDatabase(self):
        return self.movieFileMovie.query()

    def writeContentInJson(self, data, file="data.json"):
        with open(file,"w+") as outfile:
            json.dump(data, outfile)

if __name__ == '__main__':
    #do stuff
    explorer = Explorer("../../stubs/FILM_a_trier")
    lst = explorer.nameParsing(explorer.getFolderContent())
    #explorer.writeContentInJson(lst)
    explorer.addMoviesToDatabase(lst)

    print("stuff is done")

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
