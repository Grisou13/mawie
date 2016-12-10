import mimetypes
import os
import Levenshtein.StringMatcher as lev
# import mimetypes
# mimetypes.init()
from mimetypes import MimeTypes
from guessit import guessit
import sys
if __name__ == '__main__':
    sys.path.append(os.path.join(os.getcwd(), "../../"))
from mawie.models.Movie import Movie
import urllib.request
import libs.PTN as PTN
import json
import re
import mawie.models.File as modelFile
import mawie.models.Movie as modelMovie
from datetime import datetime
from mawie.explorer.googleit import googleIt
from mawie.events import *
from mawie.events.explorer import *
import time
import json

class FileContainer:
    _data = {}
    def __init__(self,data):
        self._data = data
    # def __getattr__(self, item):
    #     return self._data[item]
    # def __getattribute__(self, item):
    #     return self._data[item]
    # def __delattr__(self, item):
    #     del self._data[item]
    # def __setattr__(self, key, value):
    #     self._data[key] = value
    """
    Allows dict access, so that Eric doesn't freak out and lose it
    """
    def __delitem__(self, key):
        self._data[key]
    def __getitem__(self, key):
        return self._data[key]
    def __setitem__(self, key, value):
        self._data[key] = value

class Explorer(EventManager):

    googleIt = googleIt()
    MimeTypes = MimeTypes()
    _lastTitle = dict()
    _lastTitle["title"] = ""
    _lastTitle["imdb_id"] = ""
    count = 0
    found = dict()
    notFound = dict()

    ###################################################
    ####                                           ####
    ####            MOVIE FOLDER stuff             ####
    ####                                           ####
    ###################################################

    def getMoviesFromPath(self, path):
        path = os.path.realpath(path)
        if not os.path.exists(path):
            raise FileExistsError("The given path doesn't exists")
        if self._isFolderEmpty(path):
            raise FileExistsError("The given path is empty")

        files = []
        for r, dirs, _files in os.walk(path, topdown=False):
            for f in _files:
                path = os.path.join(r,f)
                if self._isAVideo(path):
                    # we parse the files here
                    mov =self.parseFile(path)
                    files.append(mov)

            # for d in dirs:
            #     # as Thomas said : Recursion bitch
            #     files.extend(self.getMoviesFromPath(os.path.join(r,d)))
        return self.addToDatabase(files)

    def parseFile(self, filePath):
        if not filePath == os.path.realpath(filePath):
            raise FileExistsError("File path '{}' isn't supported. Don't use symbolic links.".format(filePath))

        path, filename = os.path.split(filePath)
        parsed = self._parseName(filename)
        parsed["filePath"] = filePath
        # TODO
        # we also need to know if we found it in imdb
        return parsed

    def _parseName(self, movieName):
        mov = PTN.parse(re.sub(r'avi', "", movieName.replace(".", " ")))
        return FileContainer(guessit(movieName, {"T":mov["title"]}))

    def _secondTryParseName(self, movieName):
        return PTN.parse(re.sub(r'avi', "", movieName.replace(".", " ")))

    def _isFolderEmpty(self, folder):
        for dirpath, dirnames, files in os.walk(folder):
            if files:
                return False
            else:
                if dirnames:
                    for dpath, dnames, fls in os.walk(dirpath):
                        if(fls):
                            return False
                else:
                    return True

    def _isAVideo(self,path):
        # we get the mime type
        mime = self.MimeTypes.guess_type(urllib.request.pathname2url(path))
        # if not recognised , be a array (None, None)
        if all(v is None for v in mime):
            return False
        # and finally check if it is a video in array ex: (video, avi)
        return "video" in mime[0]


    ###################################################
    ####                                           ####
    ####               DATABASE stuff              ####
    ####                                           ####
    ###################################################
    def addSingleMovie(self,file_):
        # we try to avoid to search 20 times in a row the same title (for example for a série)
        if file_["title"] != self._lastTitle["title"]:
            fromImdb = self.googleIt.getMovieID(file_["title"])
            self._lastTitle["title"] = file_["title"]
            self._lastTitle["imdb_id"] = fromImdb
        else:
            fromImdb = self._lastTitle["imdb_id"]

        file_["imdb_id"] = fromImdb

        if file_["imdb_id"]:
            if self._addFile(f):

                foundFiles[file_["title"]] = f
                file_["parsed"] = True
                self.emit(MovieParsed(file_))
            else:
                SystemError("Cannot add file {} to database".format(file_["title"]))
        else:
            # give it a second try !
            #print(file_["title"])
            imdb_id = self.googleIt.getMovieID(file_["title"])
            #print(imdb_id)

            file_["parsed"] = False
            self.emit(MovieNotParsed(file_))
        return file_

    def addToDatabase(self, movieList):
        foundFiles = dict()
        notFoundFiles = dict()
        if len(movieList) <= 0:
            raise LookupError("The given list is empty. ")

        for f in movieList:
            res_ = self.addSingleMovie(f)
            if res_["parsed"]:
                foundFiles[res_["title"]] = res_
            else:
                notFoundFiles[res_["title"]] = res_
        self.found = foundFiles
        self.notFound = notFoundFiles
        return foundFiles, notFoundFiles
    def _getMovieByImdbId(self, imdbId):
        q = Movie.query().filter(Movie.imdb_id == imdbId)
        if not q.count():
            return False
        else:
            return q.first()

    def _addFile(self, file):
        # get the movie of the file
        mov = self._addMovie(file["imdb_id"])

        # and create a new file
        fi = modelFile.File()
        fi.path = file["filePath"]
        fi.movie_id = mov.id

        # add the relation to the movie table
        mov.files.append(fi)

        # save both the file and the movie w the new relation
        fi.save()
        mov.save()
        print("Movie added : " + file["filePath"] + " !")
        self.count += 1
        return True

    def _addMovie(self, movieId):
        # try to get the movie in the DB by its id
        mov = self._getMovieByImdbId(movieId)
        # check if movie already exists
        if not mov:  # if not, add it
            # get data from imdb (see googleIt class for details)
            foundMovie = self.googleIt.getMovieInfo(movieId=movieId)
            # we might to weird format stuff here, but don't worry we know what we do
            mov = modelMovie.Movie()
            mov.name = foundMovie.title
            mov.imdb_id = movieId
            mov.genre = ", ".join(foundMovie.genres)
            mov.desc = "\n".join(foundMovie.plots)
            mov.release = datetime.strptime(str(foundMovie.year), "%Y") if foundMovie.year is not None else None
            mov.runtime = foundMovie.runtime
            mov.actors = ", ".join(map(lambda x: x.name, foundMovie.cast_summary))
            mov.directors = ", ".join(map(lambda x: x.name, foundMovie.directors_summary))
            mov.writer = ", ".join(map(lambda x: x.name, foundMovie.writers_summary))
            mov.poster = foundMovie.poster_url
            mov.rate = foundMovie.rating
            # and save it !
            mov = mov.save()

        return mov

def w(data):
    with open('notfound.json', 'w') as outfile:
        json.dump(data, outfile)

def r():
    with open('notfound.json') as outfile:
        return json.load(outfile)

if __name__ == '__main__':
    explorer = Explorer()
    for l in r():
        r = explorer._parseName(l)
        imdb_id = explorer.googleIt.getMovieID(r["title"])
        # print(imdb_id)

    # explorer = Explorer()
    # startTime = time.process_time()
    # movies = explorer.getMoviesFromPath("../../stubs/FILM_a_trier")
    # explorer.addToDatabase(movies)
    # print("Found files ! ♥ ")
    # print(len(explorer.found))
    # print("and not found files...")
    # print(len(explorer.notFound))
    # print("Run time is ")
    # runtime = time.process_time() - startTime
    # print(str(runtime))
    # w(explorer.notFound)
    # print(r())
