from py_bing_search import PyBingWebSearch
import re
import sys
class googleIt():

    BING_API_KEY = "SjCn0rSMC6ipl8HJiI2vAYQj1REMPA+raOMPSd5K9A0"
    domainSearch = ""

    def __init__(self, domainSearch = "imdb"):
        self.domainSearch = domainSearch

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
        # pattern = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))')

        # if you give the format as http://www.imdb.com/title/tt0330373/, return the id
        # mess up if incorrect url. This is why we need a regex here
        movieId =  next(imDBlinks).split("title/")[1][:-1]

        # check wether the id is only made of min letters and digit
        assert(re.match("^[a-z0-9]*$", movieId))
        # and if it matches the right size (all id have the same size)
        assert(len(movieId) == 9)

        return movieId


    def getMovieInfo(self, movieId = "", movieTitle = ""):
        print(not not movieId)
        #assert (not movieId) or (not movieTitle)



googleItPutain = googleIt()
#myId = google.getMovieID("Harry potter 4")

myFalseId = "tt0330373"
googleItPutain.getMovieInfo(movieId = myFalseId)
googleItPutain.getMovieInfo(movieTitle = "Harry potter")
googleItPutain.getMovieInfo(movieId = myFalseId, movieTitle = "Harry potter")

"""
# pip install imdbpie

from imdbpie import Imdb
imdb = Imdb()
imdb = Imdb(anonymize=True) # to proxy requests

res = imdb.search_for_title("Very bad trip 2")
print("Pr out")
print(res)

"""
