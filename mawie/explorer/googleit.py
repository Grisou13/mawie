# pip install py_bing_search
import re
import socket

from py_bing_search import PyBingWebSearch
# from py_bing_search import PyBingWebSearch
from imdbpie import Imdb
# import Levenshtein
import re
import sys
import urllib.request

from mawie.helpers import checkInternetConnexion


class googleIt():
    BING_API_KEY = "SjCn0rSMC6ipl8HJiI2vAYQj1REMPA+raOMPSd5K9A0"
    domainSearch = ""
    imdb = object()

    def __init__(self, domainSearch="imdb"):
        self.domainSearch = domainSearch
        self.imdb = Imdb()



        # if not checkInternetConnexion():
        #     raise ConnectionError("No internet connection !")

    def _makeSearchTerm(self, movieName):
        return movieName + " :" + self.domainSearch
        # bing advanced search doesn't work w our request soooo.....
        # return "site:" + self.domainSearch + " " + movieName

    def _GetMovieResearch(self, term, limit=50, format='json'):
        bing = PyBingWebSearch(self.BING_API_KEY, term, web_only=False)
        return bing.search(limit, format)

    def _findImdbLinks(self, researchResults):

        # get all the links that contains the domainSearch name (imdb by default)
        for link in researchResults:
            if (re.search(self.domainSearch+".com", link.url)):
                return link.url
                # imdblist.append(link.url)

    def getMovieID(self, movieTitle):
        """
            Find a movie id based on the title
            movieTitle (string) is simply the movieTitle.
            Try to not use # number (ex : Harry potter 4)
            return the id as a string (ex : tt0330373)

        """

        if not isinstance(movieTitle, str):
            raise TypeError("Movie title must be a string")

        # get the fifty firsts results of a research
        researchResults = self._GetMovieResearch(self._makeSearchTerm(movieTitle))
        # find all the links from imdb
        #print(self._makeSearchTerm(movieTitle))
        #for kkk in researchResults:
        #    print(kkk.url)

        #sys.exit(movieTitle)

        imDBlinks = self._findImdbLinks(researchResults)

        # TODO make pattern to find the imdb main url (ex: http://www.imdb.com/title/tt0330373/)
        # check http://daringfireball.net/2010/07/improved_regex_for_matching_urls

        # if you give the format as http://www.imdb.com/title/tt0330373/, return the id
        # mess up if incorrect url. This is why we need a regex here
        if not imDBlinks:
            return False

        #print(imDBlinks.split("title/")[1][:-1])
        try:
            movieId = imDBlinks.split("title/")[1][:-1]
        except Exception:
            return False
            #print(imDBlinks)
            #print(movieTitle)
            #sys.exit("Status fucked up !")

        # check wether the id is only made of min letters and digit
        if not re.match("^[a-z0-9]*$", movieId):
            # we might find an id + a parameter (ex: tt1077097/fullcredit)
            if "/" in movieId:
                movieId = movieId.split("/", 1)[0]

                if re.match("^[a-z0-9]*$", movieId) and len(movieId):
                    return movieId

            return False

        # and if it matches the right size (all id have the same size)
        if not len(movieId) == 9:
            return False
        return movieId


    def getMovieInfo(self, movieId = "", movieTitle = ""):

        """
            Return information about a movie
            Movie ID (string) can be found for example in a imdb url
            Movie Title (string) is simply the move Title

            Only one parameter is required. With both parameters, we'll do a double check (but will take more time) ♥
            !! Note that using the ID return only one movie, but the Title may return many in a generator
            Prefer using a the id instead of the title

            Returned movie object properties :
            movie.imdb_id
            movie.title
            movie.type
            movie.year
            movie.tagline
            movie.plots
            movie.plot_outline
            movie.rating
            movie.genres
            movie.votes
            movie.runtime
            movie.poster_url
            movie.cover_url
            movie.release_date
            movie.certification
            movie.trailer_image_urls
            movie.directors_summary
            movie.creators
            movie.cast_summary
            movie.writers_summary
            movie.credits
            movie.trailers

        """

        def _hasNumber(inputStr):
            """
                Check if given sting contains any number (1-9).
                Return boolean

                Do you really need more details ? (this method is not used yet but migh be in ameliorations)
            """
            return any(char.isdigit() for char in inputStr)

        try:
            assert(movieId or movieTitle)
        except AssertionError:
            return False

        if not isinstance(movieTitle, str):
            raise TypeError("Movie title must be a string")

        movieTitle = movieTitle.lower()

        # BASED ON THE TITLE AND ID
        if movieTitle and movieId:
            # we search the movies with both id and title
            foundById = self.imdb.get_title_by_id(movieId)
            foundByTitle = self.imdb.search_for_title(movieTitle)

            # by title might return a list, so we iterate through it
            if isinstance(foundByTitle, list):
                for byTitle in foundByTitle:
                    # then we try to find the one that match the movie found by id
                    if byTitle.get("imdb_id") == foundById.imdb_id:
                        return foundById
                return False
            # if only one movie is found by id, then we compare it directly
            elif isinstance(foundByTitle, object):
                if foundById.imdb_id == foundByTitle.imdb_id:
                    return foundById
                else:
                    return False
            return False

        # BASED ON THE TITLE
        elif movieTitle:
            foundMovie = self.imdb.search_for_title(movieTitle)
            # if many movies found
            if(isinstance(foundMovie, list)):
                def generator(movieList):
                    for l in movieList:
                        yield self.imdb.get_title_by_id(l.get("imdb_id"))
                return generator(foundMovie)

            elif isinstance(foundMovie, object):
                return foundMovie

            return False

        # BASED ON THE ID
        elif movieId:
            # Getting a movie object by ID (should) only return one element
            foundMovie = self.imdb.get_title_by_id(movieId)
            try:
                assert isinstance(foundMovie, object)
            except AssertionError:
                return False

            return foundMovie

        else:
            # wtf
            return False



if __name__ == "__main__":

    googleItPutain = googleIt()
    res =googleItPutain.getMovieID(movieTitle="Despicable Me 2")
    print(res)
    #HarryPotter4ID = "tt0330373"
    #fightClubID = "tt0137523"

    # without parameters
    # googleItPutain.getMovieInfo()
    # with MOVIE ID
    # r = googleItPutain.getMovieInfo(movieId = fightClubID)
    # with MOVIE TITLE
    # r = googleItPutain.getMovieInfo(movieTitle = "Harry potter")
    # with MOVIE ID and MOVIE TITLE
    # r = googleItPutain.getMovieInfo(movieId = fightClubID, movieTitle = "Fight CLUB")
    pass
