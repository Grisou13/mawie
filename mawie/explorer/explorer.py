import os
import Levenshtein.StringMatcher as lev
# import mimetypes
# mimetypes.init()
from mimetypes import MimeTypes
from guessit import guessit
import sys

from mawie.events import Eventable
from mawie.events.explorer import GoogleItEvent

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
import logging
import time
import json

log = logging.getLogger("mawie")

class Explorer(Eventable):

    googleIt = googleIt()
    MimeTypes = MimeTypes()
    _lastTitle = dict()
    _lastTitle["title"] = ""
    _lastTitle["imdb_id"] = ""
    count = 0
    foundFiles = dict()
    notFoundFiles = dict()
    # main func to call.

    def parse(self, path):
        """
        Parse and stores the movies in the given folder
        :param path: Folder containing the movie files
        :return: two lists of movies. The first one is the parsed (and stores in db).
        The second list contains the unparsed files

        So the function :
        1. Get the name of every movie in the folder
        2. Parse the name of the file
        3. Get the IMDB's ID of that movie
        4. If the IMDB's ID is found, the file is in the found list and stored in the db
        6. Also stores each found movie with IMDB.com's information
        5. Returns the two lists
        """
        files = self._getMoviesFromPath(path)
        foundFiles, notFoundFiles = self._addToDatabase(files)

        # assign properties
        self.foundFiles = foundFiles
        self.notFoundFiles = notFoundFiles

        return foundFiles, notFoundFiles


    ###################################################
    ####                                           ####
    ####            MOVIE FOLDER stuff             ####
    ####                                           ####
    ###################################################

    def _getMoviesFromPath(self, path):
        path = os.path.realpath(path)
        if not os.path.exists(path):
            raise FileExistsError("The given path doesn't exists")
        if self._isFolderEmpty(path):
            raise FileExistsError("The given path is empty")

        files = []
        for r, dirs, _files in os.walk(path, topdown=False):
            for f in _files:
                path = os.path.join(r,f)
                print(path)

                if self._isAVideo(path):
                    # we parse the files here
                    files.append(self._parseFile(path))

            # for d in dirs:
            #     # as Thomas said : Recursion bitch
            #     files.extend(self.getMoviesFromPath(os.path.join(r,d)))

        return files

    def _parseFile(self, filePath):
        if not filePath == os.path.realpath(filePath):
            raise FileExistsError("File path '{}' isn't supported. Don't use symbolic links.".format(filePath))

        path, filename = os.path.split(filePath)
        parsed = self._parseName(filename)
        parsed["filePath"] = filePath

        return parsed

    def _parseName(self, movieName):
        mov = PTN.parse(re.sub(r'avi', "", movieName.replace(".", " ")))
        return guessit(movieName, {"T":mov["title"]})

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

    def _addToDatabase(self, movieList):
        foundFiles = dict()
        notFoundFiles = dict()

        if len(movieList) <= 0:
            raise LookupError("The given list is empty. ")

        for f in movieList:
            # we try to avoid to search 20 times in a row the same title (as for a série)
            if f["title"] != self._lastTitle["title"]:
                # get the imdb of that id
                fromImdb = self.googleIt.getMovieID(f["title"])
                self.emit(GoogleItEvent(f["title"]))

                self._lastTitle["title"] = f["title"]
                self._lastTitle["imdb_id"] = fromImdb
            else:
                fromImdb = self._lastTitle["imdb_id"]

            f["imdb_id"] = fromImdb

            if f["imdb_id"]:
                if self._addFile(f):

                    foundFiles[f["title"]] = f
                else:
                    SystemError("Cannot add file {} to database".format(f["title"]))
            else:
                # we could use a second try... doesn't work with the lib PTN btw
                notFoundFiles[f["title"]] = f

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
    ex = Explorer()
    ex.parse("../../stubs/FILM_a_trier")
    pass