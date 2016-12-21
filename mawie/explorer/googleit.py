# pip install py_bing_search
import re

import time
from contextlib import suppress

from bs4 import BeautifulSoup
import urllib.request
from imdbpie import Imdb
import re
import sys
from mawie.events import Listener
from mawie.events.explorer import *
import requests
# found on http://stackoverflow.com/questions/17388213/find-the-similarity-percent-between-two-strings
from difflib import SequenceMatcher

from mawie.models.Movie import Movie
import logging
log = logging.getLogger(__name__)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class GoogleIt(Listener):
    """
    This class will only search for links of a movie title and return what it found.
    @TODO You can also ask for movie Ids
    """
    # BING_API_KEY = "SjCn0rSMC6ipl8HJiI2vAYQj1REMPA+raOMPSd5K9A0"
    domainSearch = ""
    imdb = Imdb()
    _links = {}
    """
    Keeps track of all urls found with a certain url
    {
        url : [links(str)]
    }
    """
    _ids = {}
    """
    keeps track of id's found for a movie
    {
        movie title : id
    }
    """

    _searching = {}
    """
    Keeps track of all movies that are currently being searched by the explorer
    {
        movieTitle : {
            data : dict //the original search request
            found : bool
        }
    }
    """
    _searched = {}
    """
    Keeps track of all searched movies
    {
        original movie title: data
    }
    """

    def __init__(self, domainSearch="imdb", domainRegex=None):
        self.domainSearch = domainSearch
        if domainRegex is None:
            self.domainRegex = r"(?:https?\:)\/\/\w+\." + domainSearch + "\.com\/title\/([a-z]{2}[0-9a-z]{7})\/(?:.+)?"
        else:
            self.domainRegex = r""  # just put nothing

        def _doWeHaveInternet():
            try:
                req = urllib.request.Request('http://216.58.192.142')
                urllib.request.urlopen(req, timeout=1)
                return True
            except urllib.error.URLError as err:
                return False

                # if not _doWeHaveInternet():
                #     raise ConnectionError("No internet connection !")
    def sendResponse(self,title, found = False):
        """
        sends the GoogleItResponse event after a title was found
        Its a small helper
        :param found: Whether a movie was found or not
        :param title: Title of the movie
        :return: None
        """
        with suppress(ValueError,IndexError):
            del self._searching[title]  # delete the title from searching
        if title not in self._searched:#move it to the searched files
            self._searched[title] = self._searching[title]
        self.emit(GoogleItResult({"found": self._searched[title]["found"], "originalTitle": title, "data": self._searched[
            title]}))  # event contains list of files with data found on the title

    def handle(self, event):

        if isinstance(event, GoogleItSearchRequest):
            log.info("starting googleit search")
            data = event.data #data is standard guessit return
            title = data["title"]#.replace(" ","_") #just because i don't wwan tto refactor my beautiful code
            if title in self._searched:  # we already searched the movie
                log.info("movie %s was already searched",title)
                self.sendResponse(title,True)
            else:
                if title not in self._searching:
                    self._searching[title] = {"payload":data,"files": []}
                log.info("going to search movie %s",title)
                self.getMovieID(title)
                self._searching[title]["files"].append(data["filePath"])


        elif isinstance(event, NoLinkFound): #this should almost never happen
            title = event.data
            self._searched[title] = self._searching[title]
            self._searching[title]["found"] = False
            del self._searching[title]

        elif isinstance(event, TryLink):  # we need to try a link on api

            expected = event.expectedTitle #expected title is the original title of the movie. It is used to store movie info
            id = re.search(self.domainRegex, event.url).group(1)  # uses the domain search
            if expected in self._ids: #Explorer already got result if we stored it
                return
            time.sleep(.5)
            self._ids[event.expectedTitle] = id
            res = self.imdb.get_title_by_id(id)  # TODO unbind us to the imdb api

            if similar(res.title, expected) >= 0.8:  # close enough
                self._searched[expected] = {"originalTitle": expected, "files": self._searching[expected]["files"],
                                            "imdb_id": res.imdb_id, "found": True, "title": res.title,
                                            "data": res}
                self.emit(GoogleItResult(self._searched[expected]))
            else:
                if event.url in self._links[expected]:
                    with suppress(ValueError, AttributeError):#found this practical thing on the internet
                        #suppresses all raise of ValueError or AttributeError in this context
                        self._links[expected].remove(event.url)
                if len(self._links[expected]) <=0: #only when we have not checked every link can we say the google it didn't find it
                    self.emit(GoogleItResult({"originalTitle": expected, "found": False, "imdb_id": None}))

                # self.emit(TryLinkResult(event.expectedTitle,res))
                # elif isinstance(event, TryLinkResult):
                #     movieTitle = event.expected
                #     movieData = event.data
                #     if similar(movieData.title, movieTitle) >= 0.8:#close enough
                #         self.emit(GoogleItResult(movieData))
                #     else:
                #         self.emit(GoogleItResult(False))

                # bing advanced search doesn't work w our request soooo.....
                # return "site:" + self.domainSearch + " " + movieName

    def defaultHeader(self):
        return "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"

    def _findOnBing(self, title):
        res = requests.get("http://www.bing.com/search", params={"q": title + " :imdb"},
                           headers={"user-agent": self.defaultHeader()})
        links = BeautifulSoup(res.text, "html.parser").find_all('li', attrs={'class': 'b_algo'})
        for link in links:
            for l in link.find_all("a"):
                url = l.get("href")

                log.info("found url %s for title %s", url, title)
                if re.search(self.domainRegex, url):
                    #id_ = re.search(self.domainRegex, url).group(1)
                    self._links[title].append(url)
        return self._links[title]

    def _findOnDuck(self, title):
        res = requests.get("https://duckduckgo.com/html/", params={"q": title + " :imdb"},
                           headers={"user-agent": self.defaultHeader()})
        links = BeautifulSoup(res.text, "html.parser").find_all("a", attrs={"class": u"result__a"}, href=True)
        for link in links:
            url = link.get("href")

            log.info("found url %s for title %s",url,title)
            if re.search(self.domainRegex, url):  # it's a valid url for the domain we want to search data in
                #id_ = re.search(self.domainRegex, url).group(1)
                self._links[title].append(url)
        return self._links[title]

    def _GetMovieResearch(self, movieTitle, limit=50, format='json', bing=False):
        h = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        if not bing:
            # term = self._makeSearchTerm(movieTitle)

            res = requests.get("https://duckduckgo.com/html/", params={"q": movieTitle + " :imdb"},
                               headers={"user-agent": h})
            # res.encoding
            r = BeautifulSoup(res.text, "html.parser").find_all("a", attrs={"class": u"result__a"}, href=True)
            return r
        elif bing:
            term = "http://www.bing.com/search?q=" + movieTitle + " :imdb"
            res = requests.get(term, headers={"user-agent": h})
            r = BeautifulSoup(res.text, "html.parser").find_all('li', attrs={'class': 'b_algo'})
            return r
        else:
            return False

            # try:
            #    fp = urllib.request.urlopen(term)
            # except urllib.error.HTTPError as e:
            #    print(e)
            #    term = self._makeSearchTerm(movieTitle, domain=False)
            #    try:
            #        fp = urllib.request.urlopen(term)
            #    except urllib.error.HTTPError:
            #        print(term)
            #        sys.exit("fuuuuu")
            # r = fp.read().decode("utf8")
            # fp.close()
            # return

    def _findImdbLinks(self, researchResults, bing=False):
        if not bing:
            # get all the links that contains the domainSearch name (imdb by default)
            for link in researchResults:
                if (re.search(self.domainSearch + ".com", link.get("href"))):
                    return link.get("href")
                    # imdblist.append(link.url)
        elif bing:
            for link in researchResults:
                if (re.search(self.domainSearch + ".com", link.find("a").get("href"))):
                    return link.find("a").get("href")

    def _searchMovie(self, title):
        query = Movie.query().filter(Movie.name == title)
        log.info("searching db first to see if we dont already have the movie %s",title)
        if query.count():
            log.info("already have it")
            self.emit(GoogleItResult(query.first()))
        else:
            self._links[title] = []
            log.info("searching .... ")
            try:
                time.sleep(.3)  # add some sleep before anything else can be done, so that we don't get ip banned
                self._findOnDuck(title) #links found are stored in self._links[title]

            except: #if something went wrong with duck duck go try bing scraping
                time.sleep(.2)
                self._findOnBing(title) #links found are stored in self._links[title]
            finally: #now try the links
                if len(self._links[title]):
                    for link in self._links[title].copy():
                        self.emit(TryLink(link,title))

                else:#couldn't find any link ???
                    self.emit(NoLinkFound(title))

    def getMovieTitle(self, movieId):
        pass

    def getMovieID(self, movieTitle):
        """
        Find a movie id based on the title
        movieTitle (string) is simply the movieTitle.
        Try to not use # number (ex : Harry potter 4)
        return the id as a string (ex : tt0330373)
        """

        if not isinstance(movieTitle, str):
            raise TypeError("Movie title must be a string")

        if hasattr(self, "emit"):  # use events and async to get movie data
            log.info("searching for movie %s", movieTitle)
            self._searchMovie(movieTitle)
        else:  # otherwise do it in a blocking way
            # get the ffirst page of a research
            researchResults = self._searchMovie(movieTitle)
            return researchResults
            # find all the links from imdb
            # imDBlinks = self._findImdbLinks(researchResults, bing=secondTry)

            # TODO make pattern to find the imdb main url (ex: http://www.imdb.com/title/tt0330373/)
            # check http://daringfireball.net/2010/07/improved_regex_for_matching_urls

            # if you give the format as http://www.imdb.com/title/tt0330373/, return the id
            # mess up if incorrect url. This is why we need a regex here
            # if not imDBlinks:
            #     self.emit(GoogleItResult([movieTitle, False]))
            #
            # #print(imDBlinks.split("title/")[1][:-1])
            # try:
            #     movieId = imDBlinks.split("title/")[1][:-1]
            # except Exception:
            #     self.emit(GoogleItResult([movieTitle, False]))
            #
            #
            # # check wether the id is only made of min letters and digit
            # if not re.match("^[a-z0-9]*$", movieId):
            #     # we might find an id + a parameter (ex: tt1077097/fullcredit)
            #     if "/" in movieId:
            #         movieId = movieId.split("/", 1)[0]
            #
            #         if not re.match("^[a-z0-9]*$", movieId) and len(movieId):
            #             self.emit(GoogleItResult([movieTitle, False]))
            #     else:
            #         self.emit(GoogleItResult([movieTitle, False]))
            #
            # # and if it matches the right size (all id have the same size)
            # if len(movieId) == 9:
            #     # print("ho putain 4")
            #     self.emit(GoogleItResult([movieTitle, False]))
            #
            #
            # self.emit(GoogleItResult([movieTitle, movieId]))

            # return movieId

    def getMovieInfo(self, movieId="", movieTitle=""):

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
            assert (movieId or movieTitle)
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
            if (isinstance(foundMovie, list)):
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
    googleItPutain = GoogleIt()
    # todo unicode stuff
    # https://pypi.python.org/pypi/Unidecode
    # res = googleItPutain.getMovieID(movieTitle="La guerre des étoiles")
    # print(res)
    # HarryPotter4ID = "tt0330373"
    fightClubID = "tt0137523"

    # without parameters
    # googleItPutain.getMovieInfo()
    # with MOVIE ID
    # r = googleItPutain.getMovieInfo(movieId = fightClubID)
    # with MOVIE TITLE
    # r = googleItPutain.getMovieInfo(movieTitle = "Harry potter")
    # with MOVIE ID and MOVIE TITLE
    r = googleItPutain.getMovieInfo(movieId=fightClubID, movieTitle="Fight CLUB")
    print(r.title)
    print(r.plots)
    print(r.release_date)
    pass
