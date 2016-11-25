import os
import sys
from functools import reduce

import Levenshtein.StringMatcher as lev

from app.models.Movie import Movie
import mimetypes
import urllib.request
mimetypes.init()
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
    maxRatio = 20
    allowedData=["path"]
    def __init__(self, path=None):
        self.movieFileConnector = File



        self._cacheList = []
        self._ratios = []  # allows to calulate the average for all movie filename rations
        self._list = []
        self._dirtyList = []
        self._cleanList = []
        self.path = None
        if path is not None :
            assert os.path.exists(path), 'The path does not exist'
            if (self.checkDirIfEmpty(path)):
                raise FileNotFoundError("No file has been found in the {} path".format(path))
            self.path = path
            self.getFolderContent(path) #directly parse the directory



        # r = self.movieModel.query()
        # print(r)
    @property
    def files(self):
        return self._list

    @files.setter
    def updateList(self, newList):
        self._cacheList.append(self._list)
        self._list = newList
    @property
    def parsedFiles(self):
        return self._cleanList
    @parsedFiles.setter
    def s(self,val):
        self._cleanList = val
    @property
    def nonParsedFiles(self):
        return self._dirtyList

    @parsedFiles.setter
    def s(self, val):
        self._dirtyList = val
    @property
    def initialList(self):
        assert len(self._cacheList) < 1, "You should use getFolderContent first, or populate the .files property"
        return self._cacheList[0] # return the first element of the cache list
    @property
    def avgFilenameRatio(self):
        return (reduce(lambda x, y: x + y, self._ratios) / len(self._ratios))
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
    def _checkFileIsVideo(self,path):
        url = urllib.request.pathname2url(path)
        mime = mimetypes.guess_type(url)
        if not 0 in mime:
            return False
        print(mime[0])
        print(path)
        return "video" in mime[0]
    def _extractFilesIn(self, path):
        assert os.path.exists(path) #just check it okey
        files = []
        for r, dirs, _files in os.walk(path, topdown=False):  # don't car about order

            for f in _files :
                path = os.path.join(r,f)
                if self._checkFileIsVideo(path):
                    files.append(self._parseFromPath(path))
            for d in dirs:
                path = os.path.join(r, d)
                print(path)
                files.extend(self._extractFilesIn(path))  # recursion bitch
        return files

    def _parseFromPath(self, filepath):
        assert filepath == os.path.realpath(filepath), "need full path of file, use os.path.realpath from root"
        path, filename = os.path.split(filepath)
        data = self._parseName(filename)
        data["path"] = filepath
        r = lev.ratio(data["title"], filename) * 100 #allows to get in percent...easier to understand
        self._ratios.append(r)
        data["ratio"] = r
        # dumb if to implement later or directly assign it to dict
        if r > self.maxRatio: # if the name is far from the filename, we can consider it parsed
            #we try to construct the most plosible title with the filename, the parsed name, and a few iterations of the filename
            t = data["title"]
            data["oldTitle"] = t #just get it, maybe we need it
            data["title"] = lev.median_improve(t,[t,filename,PTN.ptn.excess_raw,t.strip(),t.lower()]) # TODO async this, since they are very processor heavy operations
            data["parsed"] = True
        else:
            data["parsed"] = False

        #print(data["title"],":",data["ratio"],"[",data["oldTitle"] if data["parsed"] else "not-parsed","]", " ----- ", filename)
        return data

    def commit(self,list=[], rename=False):
        for f in self.parsedFiles if len(list) <=0 else list:

            self._addFile(data=f, rename=rename)
    def _searchMovie(self,title):
        print("searching movie with title",title)
        return Movie.get(1) #append to n1 movie
    def _addFile(self, data = None, filepath = None, rename = False):
        if filepath is not None:
            print(filepath)
            data = self._parseFromPath(filepath)
        elif data is not None:
            data = data
        else:
            raise Exception("You didnt provide any data to add to database")
        if "title" not in data:
            raise Exception("the file must contain a title")
        if "path" not in data:
            raise Exception("the file must contain a path")

        if rename:
            os.rename(data["path"], os.path.join(os.path.basename(data["path"], data["title"])))  # rename the file on insert to something more readable with only the title
        movie = self._searchMovie(data["title"])
        # delete unnecessary data
        for el in data.copy():
            if el not in self.allowedData:
                del data[el]
        # replace any list in the data by an array (['FRENCH', 'BDRip'] => 'FRENCH, BDRip')
        for k, v in data.items():
            if (isinstance(v, list)):
                # yeah i know, python is weird sometimes
                data[k] = ", ".join(v)
            elif (not isinstance(v, str) and not isinstance(v, int)):
                raise TypeError("Movie data format not conform")
        # check if the path isn't already in the db
        # if len(self.movieFileConnector.query(self.movieFileConnector.path.distinct()).filter(
        #                 self.movieFileConnector.path == data["path"]).all()) > 0:
        #     raise Exception("The file already exists")
        data["movie"] = movie
        file = self.movieFileConnector(**data)
        print(file)
        return file.save()

    def getFolderContent(self, path=None):
        if path is None:
            path = self.path

        # check if exists
        assert os.path.exists(path)

        path = os.path.realpath(path)
        self.path = path
        files = self._extractFilesIn(path)

        self._list = files
        self._cleanList = list(filter(lambda f:f["parsed"]==True,files))
        self._dirtyList = list(filter(lambda f:f["parsed"]==False,files))

        return self._list, self._cleanList, self._dirtyList

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

    print(explorer.avgFilenameRatio)

    #lst = explorer.nameParsing(explorer.getFolderContent())

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
