import os
# import Levenshtein.StringMatcher as lev
# import mimetypes
# mimetypes.init()
from mimetypes import MimeTypes
from guessit import guessit
import sys
#from time import sleep as wait
from mawie.models import File

if __name__ == '__main__':
    sys.path.append(os.path.join(os.getcwd(), "../../"))

from mawie.events import Eventable, Listener
from mawie.events.explorer import ExplorerParsingRequest, ExplorerParsingResponse, GoogleItSearchRequest, GoogleItResult, GoogleItResponse, \
    MovieNotParsed, MovieParsed

from mawie.models.Movie import Movie
import urllib.request
import libs.PTN as PTN
import json
import re
import mawie.models.File as modelFile
import mawie.models.Movie as modelMovie
from datetime import datetime
from mawie.explorer.googleit import GoogleIt
import logging
import time
import json

log = logging.getLogger("mawie")


class Explorer(Listener):
    """
    When using Explorer as a listener it will only send back ExplorerResponse for every file that was *parsed*.
    At the begining of the explorer task, it will send all movies that were detected. Consider them as *non parsed*
    """
    googleIt = GoogleIt()
    MimeTypes = MimeTypes()
    _lastTitle = {"title":"","imdb_id":""}

    count = 0
    foundFiles = dict()
    notFoundFiles = dict()

    # _notParsed = {}
    # """
    # Keeps track of all non parsed files
    # {
    #     file: {
    #         links : [
    #             {
    #                 tried : bool,
    #                 url: str,
    #                 data : None | {imdbpie.objects.Title}
    #             }
    #         ]
    #     }
    # }
    # """
    # _parsed = {}
    # """
    # keeps track of all parsed files
    # {
    #   file : {
    #     root: str,
    #
    #     data : None | dict, # best data according to googleit
    #     title : None | str,
    #     found : bool
    #   }
    # }
    # """
    _parse = {}
    """
    keeps track of all files being currently parsed
    {
        title : {
            data : guessit data,
            files : [ filepath strings (realpaths) ]
            root : root path of the file (File.base)
        }
    }
    """
    def handle(self, event):
        if isinstance(event, ExplorerParsingRequest):
            path = event.data
            self.parse(path)
            #self.emit(ExplorerParsingResponse(event, res))

        if isinstance(event, GoogleItResult):
            #now that we got a response, we need to check the payload and get the file that was originaly searched
            movieData = event.data
            title = movieData["originalTitle"] if "originalTitle" in movieData else movieData["title"]
            if isinstance(movieData,Movie):
                self._parse[title]["data"] = movieData
                self._parse[title]["found"] = True
                for f in self._parse[title]["files"]:
                    self.emit(MovieParsed(f))
                #send back the response for a whole title ... can be usefull
                self.emit(ExplorerParsingResponse(None, self._parse[title]))  # send back the filepath that was parsed
            elif movieData["found"]:
                self._parse[title]["data"] = movieData["data"]
                self._parse[title]["found"] = True
                self._createMovieFromData(self._parse[title])
                for f in self._parse[title]["files"]:
                    self.emit(MovieParsed(f))
                self.emit(ExplorerParsingResponse(None, self._parse[title])) # TODO verify if we parsed all the files corresponding to the title before sending back
            else:
                self._parse[title]["data"] = None
                self._parse[title]["found"] = False
    def _createMovieFromData(self,data):

        files = data["files"]
        root = data["root"]
        foundMovie = data["data"]
        if Movie.query().filter(Movie.imdb_id == foundMovie.imdb_id).count():
            log.info("film %s [imdb_id = %s] already exists",foundMovie.title,foundMovie.imdb_id)
            return
        mov = Movie()
        mov.name = foundMovie.title #["title"]
        mov.imdb_id = foundMovie.imdb_id
        mov.genre = ", ".join(foundMovie.genres) if foundMovie.genres is not None else None
        mov.desc = "\n".join(foundMovie.plots) if getattr(foundMovie,"plots") is not None else None
        mov.release = datetime.strptime(str(foundMovie.year), "%Y") if foundMovie.year is not None else None
        mov.runtime = foundMovie.runtime if getattr(foundMovie,"runtime") is not None else None
        #TODO add models for this or fake ones like phurni
        mov.actors = ", ".join(map(lambda x: x.name, foundMovie.cast_summary)) if getattr(foundMovie,"cast_summary") is not None else None
        mov.directors = ", ".join(map(lambda x: x.name, foundMovie.directors_summary)) if getattr(foundMovie,"directors_summary") is not None else None
        mov.writer = ", ".join(map(lambda x: x.name, foundMovie.writers_summary)) if getattr(foundMovie,"writers_summary") is not None else None
        mov.poster = foundMovie.poster_url if getattr(foundMovie,"poster_url") is not None else None
        mov.rate = foundMovie.rating if getattr(foundMovie,"rating") is not None else None
        # and save it !
        mov = mov.save()
        log.info("adding %s to the database", mov)
        for f in files:
            fi = File()
            fi.path = f
            fi.base = root
            mov.files.append(fi) #add the file
            mov.save()
            fi.save()
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
        if hasattr(self,"emit"):
            files = self._getMoviesFromPath(path)#first get all the files
            for f in files: #get the data back to the gui
                self.emit(MovieNotParsed(f["filePath"]))
            for f in files:#then ask to get the movie data
                self.emit(GoogleItSearchRequest(f))
        else:
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
        """
        Will get all files and parse them with guessit.
        The returned files will have the following info : title,filePath.
        More info are returned with guessit, just dump it to take a look. The most important is the title though
        If the explorer is bound to an event manager and that event manager has added the emit method,
        then explorer will use events to get data back and force.

        :param path:
        :return: list
        """
        path = os.path.realpath(path)
        if not os.path.exists(path):
            raise FileExistsError("The given path doesn't exists")
        if self._isFolderEmpty(path):
            raise FileExistsError("The given path is empty")
        rootpath = path
        files = []
        for r, dirs, _files in os.walk(path, topdown=False):
            for f in _files:
                path = os.path.join(r,f)
                if self._isAVideo(path):
                    # we parse the files here
                    parsed = self._parseFile(path)
                    files.append(parsed)
                    if hasattr(self,"emit"): #if the explorer is bound to the App and uses event, then use them, otherwise we just return files
                        if parsed["title"] in self._parse:#check if haven't already parsed the same movie title (it can be a series)
                            if path not in self._parse[parsed["title"]]["files"]: #only add the file if we don't have it
                                self._parse[parsed["title"]]["files"].append(path)
                            #self.emit(GoogleItSearchRequest(parsed))
                        else:
                            #if self._parsed[""]
                            self._parse[parsed["title"]] = {"data": parsed, "root": rootpath,"files":[path]}
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
            raise ValueError("The given list is empty. ")

        for f in movieList:

            # we try to avoid to search 20 times in a row the same title (as for a series)
            if f["title"] != self._lastTitle["title"]:
            # get the imdb of that id
                fromImdb = self.googleIt.getMovieID(f["title"])
            #ici
                self._lastTitle["title"] = f["title"]
                self._lastTitle["imdb_id"] = fromImdb

            else:
                self.emit(GoogleItResult([self._lastTitle["title"], self._lastTitle["imdb_id"]]))


            continue #anyway

        #else:
            #self.emit(GoogleItResponse[self._lastTitle["title"], self._lastTitle["imdb_id"]])
            #continue
                #fromImdb = self._lastTitle["imdb_id"]

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
