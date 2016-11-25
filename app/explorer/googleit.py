# pip install py_bing_search
import re

from py_bing_search import PyBingWebSearch
#from py_bing_search import PyBingWebSearch
from imdbpie import Imdb
import Levenshtein
import re
import sys


class googleIt():

    BING_API_KEY = "SjCn0rSMC6ipl8HJiI2vAYQj1REMPA+raOMPSd5K9A0"
    domainSearch = ""
    imdb = object()

    def __init__(self, domainSearch = "imdb"):
        self.domainSearch = domainSearch
        self.imdb = Imdb()

    def _makeSearchTerm(self, movieName):
        return movieName +" :" +self.domainSearch
        # bing advanced search doesn't work w our request soooo.....
        #return "site:" + self.domainSearch + " " + movieName

    def _GetMovieResearch(self, term, limit=50, format='json'):

        bing = PyBingWebSearch(self.BING_API_KEY, term, web_only=False)
        return bing.search(limit, format)

    def _findImdbLinks(self, researchResults):
        # get all the links that contains the domainSearch name (imdb by default)
        for link in researchResults:

            if(re.search(self.domainSearch, link.url)):
                yield link.url
                #imdblist.append(link.url)


    def getMovieID(self, movieTitle):
        assert isinstance(movieTitle, str)
        # get the fifty firsts results of a research
        researchResults = self._GetMovieResearch(self._makeSearchTerm(movieTitle))
        # find all the links from imdb
        imDBlinks = self._findImdbLinks(researchResults)

        # TODO make pattern to find the imdb main url (ex: http://www.imdb.com/title/tt0330373/)
        # check http://daringfireball.net/2010/07/improved_regex_for_matching_urls

        # if you give the format as http://www.imdb.com/title/tt0330373/, return the id
        # mess up if incorrect url. This is why we need a regex here
        movieId =  next(imDBlinks).split("title/")[1][:-1]

        # check wether the id is only made of min letters and digit
        assert(re.match("^[a-z0-9]*$", movieId))
        # and if it matches the right size (all id have the same size)
        assert(len(movieId) == 9)

        return movieId

    def getMovieImage(self, movieId = "", movieTitle = ""):
        pass


    def getMovieInfo(self, movieId = "", movieTitle = ""):
        """
            Return information about a movie
            Movie ID (string) can be found for example in a imdb url
            Movie Title (string) is simply the move Title
            Only one parameter is required. With both parameters, we'll do a double check ♥
            !! Note that using the ID return only one movie, but the Title may return many

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
                Do you really need more details ?
            """
            return any(char.isdigit() for char in inputStr)

        try:
            assert(movieId or movieTitle)
        except AssertionError:
            return False

        assert isinstance(movieTitle, str)
        movieTitle = movieTitle.lower()

        if movieTitle and movieId:
            """if(movieId == l.get("imdb_id")):
                theChosenOne = self.imdb.search_for_title(movieId)
                print(theChosenOne)
                print("welcome to the grind")
                print(theChosenOne.title)
                print(theChosenOne.type)
                print(theChosenOne.year)
                print(theChosenOne.genres)
                print(theChosenOne.trailers)
                print(theChosenOne.poster_url)


            sys.exit("fuck tamère")"""
        elif movieTitle:
            foundMovie =  self.imdb.search_for_title(movieTitle)
            # if many movies found
            if(isinstance(foundMovie, list)):

                def generator(movieList):
                    for l in movieList:
                        yield self.imdb.get_title_by_id(l.get("imdb_id"))

                for m in generator(foundMovie):
                    print(m)
                    print(m.title)
                    print(m.type)
                    print(m.year)

                return "nique ta mère"

        elif movieId:
            return self.imdb.get_title_by_id(movieId)


            """
            # check if found movie correspond to the given one (if one given)
            if movieTitle:
                # if the given movie name contains a #, we won't do a Levenshtein
                # Harry Potter 4 === Harry Potter and the Goblet of Fire
                if not _hasNumber(movieTitle):
                    # If no # in it, we'd do a little Levenshtein distance mesure
                    # both movies name are in lowercase
                    if Levenshtein.distance(foundMovieTitle, movieTitle) > 3:
                        raise ValueError("Given movie title doesn't match the id.")
            """

        else:
            #wtf
            return False



if __name__ == "__main__":
    googleItPutain = googleIt()
    #myId = google.getMovieID("Harry potter 4")

    myFalseId = "tt0330373"
    DonnotSpeakAboutIt = "tt0137523"

    #googleItPutain.getMovieInfo(movieId = DonnotSpeakAboutIt)
    googleItPutain.getMovieInfo(movieTitle = "Harry potter")
    #googleItPutain.getMovieInfo(movieId = DonnotSpeakAboutIt, movieTitle = "Fight CLUB")
    #googleItPutain.getMovieInfo()

"""
# pip install imdbpie

from imdbpie import Imdb
imdb = Imdb()
imdb = Imdb(anonymize=True) # to proxy requests

res = imdb.search_for_title("Very bad trip 2")
print("Pr out")
print(res)
"""
