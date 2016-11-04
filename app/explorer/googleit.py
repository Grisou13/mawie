import json
import urllib.request
import sys

"""
    PLEASE READ HERE FIRST

    the duckduckgo api that I'm using doesn't handle the "non obvious queries"
    I still need to have a look at it. We might use another research api.

    RTM here
    https://api.duckduckgo.com/api
    and have a live example (that doesn't work (that's the point...))
    https://duckduckgo.com/?q=very%20bad%20trip%3Aimdb&format=json

    HF ! 
""""



#http://api.duckduckgo.com/?q=x&format=json

# mv = "very bad trip"
# q = "http://duckduckgo.com/?q="+mv+"+%3Aimdb&format=json"
#
# webURL = urllib.request.urlopen(q)
# data = webURL.read()
# encoding = webURL.info().get_content_charset('utf-8')
# print(data)
# print("oooo")
# json.loads(data.decode(encoding))
#

class googleIt():


    # toCheck
    # it fails when you set @property here
    def getAMove(self, movieTitle):
        q = self.formatUrlForQuery(movieTitle)
        print(q)

    def formatUrlForQuery(self, movieTitle, website="imdb", format="json"):
        movieTitle = movieTitle.replace(" ", "%20")
        return "http://duckduckgo.com/?q=" + movieTitle + "+%3A" + website + "&format=" + format


    def getFirstWebsite(self, jsonResult):
        pass

    def checkWebsiteURl(self, url, website="imdb"):
        pass

cls = googleIt()
cls.getAMove("very bad trip")
