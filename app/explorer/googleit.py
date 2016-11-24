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
            Return the IMDB's info of a movie

            movieId (string) is the IMDB id (can be found in a IMDB url)
            movieTitle (sting) is simple the movie
            Only one parameter is required.
            If both are given, we'll  check if movieId correspond to the movieTitle
        """
        def _hasNumber(inputStr):
            """
                Check if given sting contains any number (1-9).
                Return boolean
                Do you really need more details ?
            """
            return any(char.isdigit() for char in inputStr)

        assert(movieId or movieTitle)
        assert isinstance(movieTitle, str)
        movieTitle = movieTitle.lower()

        if movieTitle:

            foundMovieInfo = self.imdb.search_for_title(movieTitle)
            print(foundMovieInfo)
            print(type(foundMovieInfo))
            sys.exit("")

            if isinstance(foundMovieInfo, list):
                pass
                
            #print(foundMovieInfo)
            for l in foundMovieInfo:

                print(l)

                #print(type(self.getMovieInfo(l.get("imdb_id"))))
                #print(l.get("imdb_id"))
                #print(self.getMovieInfo(l.get))
                #print(self.imdb.get_title_by_id(l.get("imdb_id")))

        elif movieId:
            foundMovieTitle = self.imdb.get_title_by_id(movieId)
            foundMovieInfo = self.imdb.search_for_title()

            print()

            foundMovieTitle = foundMovieInfo.title.lower()
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
            return foundMovieInfo

        # if no given id, then try to find with title

        else:
            #wtf
            return False



if __name__ == "__main__":
    googleItPutain = googleIt()
    #myId = google.getMovieID("Harry potter 4")

    myFalseId = "tt0330373"
    DonnotSpeakAboutIt = "tt0137523"

    #googleItPutain.getMovieInfo(movieId = myFalseId)
    googleItPutain.getMovieInfo(movieTitle = "Harry potter")
    #googleItPutain.getMovieInfo(movieId = DonnotSpeakAboutIt, movieTitle = "Fight CLUB")
    googleItPutain.getMovieInfo()

"""
# pip install imdbpie

from imdbpie import Imdb
imdb = Imdb()
imdb = Imdb(anonymize=True) # to proxy requests

res = imdb.search_for_title("Very bad trip 2")
print("Pr out")
print(res)
"""
