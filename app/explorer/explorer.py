import os
import Levenshtein.StringMatcher as lev
# import mimetypes
# mimetypes.init()
from mimetypes import MimeTypes
from guessit import guessit
import sys
if __name__ == '__main__':
    sys.path.append(os.path.join(os.getcwd(), "../../"))
from app.models.Movie import Movie
import urllib.request
import PTN
import json
import re
import app.models.File as modelFile
import app.models.Movie as modelMovie
from datetime import datetime
from app.explorer.googleit import googleIt


class Explorer():

    googleIt = googleIt()
    MimeTypes = MimeTypes()
    _lastTitle = dict()
    _lastTitle["title"] = ""
    _lastTitle["imdb_id"] = ""

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
                    files.append(self._parseFile(path))
            for d in dirs:
                # as Thomas said : Recursion bitch
                files.extend(self.getMoviesFromPath(os.path.join(r,d)))

        return files

    def _parseFile(self, filePath):
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
        return guessit(movieName, {"T":mov["title"]})

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

    def addToDatabase(self, movieList):
        foundFiles = dict()
        notFoundFiles = dict()
        if len(movieList) <= 0:
            raise LookupError("The given list is empty. ")

        for f in movieList:
            # we try to avoid to search 20 times in a row the same title (for example for a série)
            if f["title"] != self._lastTitle["title"]:
                fromImdb = self.googleIt.getMovieID(f["title"])
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
                notFoundFiles[f["title"]] = f


    def _getMovieByImdbId(self, imdbId):
        q = Movie.query().filter(Movie.imdb_id == imdbId)
        if not q.count():
            return False
        else:
            return q.first()


    def _addFile(self, file):
        # get the movie linked to the found file
        mov = self._getMovieByImdbId(file["imdb_id"])
        # if the movie doesn't exists, we create it !
        if not mov:
            # get data from imdb (see googleIt class for details)
            foundMovie = self.googleIt.getMovieInfo(movieId = file["imdb_id"])
            # we might to weird format stuff here, but don't worry we know what we do
            mov = modelMovie.Movie()
            mov.name = foundMovie.title
            mov.imdb_id = file["imdb_id"]
            mov.genre = ", ".join(foundMovie.genres)
            mov.desc =  "\n".join(foundMovie.plots)
            mov.release = datetime.strptime(str(foundMovie.year),"%Y") if foundMovie.year is not None else None
            mov.runtime = foundMovie.runtime
            mov.actors  = ", ".join(map(lambda x: x.name, foundMovie.cast_summary))
            mov.directors = ", ".join(map(lambda x: x.name, foundMovie.directors_summary))
            mov.writer  = ", ".join(map(lambda x: x.name, foundMovie.writers_summary))
            mov.poster = foundMovie.poster_url
            mov.rate = foundMovie.rating

        # add the relation to the movie table
        # mov.files.append(file)
        fi = modelFile.File()
        fi.path = file["filePath"]
        fi.movie.append(mov)

        print(file["title"])
        print(file["filePath"])
        print(file["imdb_id"])
        fi.save()
        mov.save()
        sys.exit("FOOOOOO")

        #newFile = modelFile.File()
        #print(fromImdb)
        #print(dict(file))
        return True

    def _addMovie(self, movie):
        # check if movie already exists
        # if not, add it
        pass



if __name__ == '__main__':
    explorer = Explorer()
    movies = explorer.getMoviesFromPath("../../stubs/FILM_a_trier")
    explorer.addToDatabase(movies)
