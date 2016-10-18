import os
import sys

if __name__ == '__main__':
    sys.path.append(os.path.join(os.getcwd(), "../../"))
import PTN
import json
import re

from app.models.File import File


# import app.models.Movie

class Explorer():
    # database connector uses SQLAlchemy
    movieFileMovie = object()

    def __init__(self, path=None):

        if (path is not None) and os.path.exists(path) is False:
            raise IsADirectoryError("Film directory '{}' not found".format(path))
        else:
            self._list = None  # no list by default, unless a path is supplied
            self.getFolderContent(path)

        if (self.checkDirIfEmpty(path)):
            raise FileNotFoundError("No file has been found in the {} path".format(path))

        self.path = path
        self.movieFileConnector = File

        self._cleanList = []
        self._dirtyList = []

        self._movieCache = []

        # r = self.movieModel.query()
        # print(r)

    def checkDirIfEmpty(self, dir):
        """ Check for file in folder and subfolder (only 1 folder of depth) """
        # TODO need to be tested in a folder with files ONLY in subfolder
        f = True
        for dirpath, dirnames, files in os.walk(dir):
            if files:
                # Found
                f = False
            if not files:
                # Not found but....
                if dirnames:
                    for dpath, dnames, fls in os.walk(dirpath):
                        if fls:
                            # Found in subfolde ! :)
                            f = False
        return f

    def extractFilesIn(self, path):
        assert os.path.exists(path) #just check it okey
        files = []

        for r, dirs, files in os.walk(path, topdown=False):  # don't car about order
            for f in files:
                files.append(self._parseFromPath(f))
            for d in dirs:
                files.extend(self.extractFilesIn(d))  # recursion bitch
        return files

    def _parseFromPath(self, filepath):
        path, filename = os.path.basename(filepath)
        data = self._parseName(filename)
        data["path"] = filepath
        data["parsed"] = True
        # dumb if to implement later or directly assign it to dict
        if False is True:  # TODO implement levenstein verification if the title is almost the same as filename, then consider it parsed or not
            data["parsed"] = False

        return data

    def commit(self, rename=False):
        for f in self._list:
            self._addFile(f, rename)

    def _addFile(self, filepath, rename):

        data = self._parseFromPath(filepath)
        if rename:
            os.rename(data["path"], os.path.join(os.path.basename(data["path"], data[
                "title"])))  # rename the file on insert to something more readable with only the title
        if ("episodeName" in data):
            del data["episodeName"]
        if ("proper" in data):
            del data["proper"]
        """try:
            k = data["title"]
        except (IndexError, KeyError):
            print(data)
            sys.exit("decomment that ")"""
        # replace any list in the data by an array (['FRENCH', 'BDRip'] => 'FRENCH, BDRip')
        for k, v in data.items():
            if (isinstance(v, list)):
                # yeah i know, python is weird sometimes
                data[k] = ", ".join(v)
            elif (not isinstance(v, str) and not isinstance(v, int)):
                raise TypeError("Movie data format not conform")
        # check if the path isn't already in the db
        if len(self.movieFileConnector.query(self.movieFileConnector.path.distinct()).filter(
                        self.movieFileConnector.path == data["path"]).all()) > 0:
            raise Exception("The file already exists")
        return self.movieFileConnector.create(**data)

    def getFolderContent(self, path=None):
        if path is None:
            path = self.path
        # check if exists
        assert os.path.exists(path)
        files = self.extractFilesIn(path)
        self._list = filter(lambda f:f["parsed"]==True,files)
        return files,filter(lambda f:f["parsed"]==False,files)

    def _parseName(self, movName):
        m = PTN.parse(movName.replace(".", " "))
        return m

    def nameParsing(self, movieList=None):
        if movieList is None and self._list is None:
            raise Exception("You need to supply a list of movies or getFolderContent")
        if movieList is None:
            movieList = self._list

        # TODO in folder, return the files in it and not the folder !
        if not (isinstance(movieList, list)):
            raise TypeError("Expecting a list")
        cleanMovieList = {}
        for dirtyMovie in movieList:
            # TODO optimise REGEX parsing (PTN/patterns.py)
            parsed = PTN.parse(dirtyMovie.replace(".", " "))
            print(dirtyMovie)
            cleanMovieList[parsed['title']] = parsed
        return cleanMovieList

    def addMoviesToDatabase(self, movieList):
        assert isinstance(movieList, dict)
        # TODO add the path of te movie :)))))
        # WITH NORMAL SLASH
        for movie, data in movieList.items():
            # useless data from the parser
            if ("episodeName" in data):
                del data["episodeName"]
            if ("proper" in data):
                del data["proper"]
            """try:
                k = data["title"]
            except (IndexError, KeyError):
                print(data)
                sys.exit("decomment that ")"""
            # replace any list in the data by an arrray (['FRENCH', 'BDRip'] => 'FRENCH, BDRip')
            for k, v in data.items():
                if (isinstance(v, list)):
                    # yeah i know, python is weird sometimes
                    data[k] = ", ".join(v)
                elif (not isinstance(v, str) and not isinstance(v, int)):
                    raise TypeError("Movie data format not conform")
            # print data if you want to know why i used the **kwargs

            moveFile = self.movieFileConnector(**data).save()

    def getAllMoviesFromDatabase(self):
        return self.movieFileConnector.query()

    def writeContentInJson(self, data, file="data.json"):
        with open(file, "w+") as outfile:
            json.dump(data, outfile)


if __name__ == '__main__':
    # get stuff done
    explorer = Explorer("../../stubs/FILM_a_trier")
    lst = explorer.nameParsing(explorer.getFolderContent())

    # explorer.addMoviesToDatabase(lst)
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
