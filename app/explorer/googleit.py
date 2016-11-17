

'''
    PLEASE READ HERE FIRST

    the duckduckgo api that I'm using doesn't handle the "non obvious queries"
    I still need to have a look at it. We might use another research api.

    RTM here
    https://api.duckduckgo.com/api
    and have a live example (that doesn't work (that's the point...))
    https://duckduckgo.com/?q=very%20bad%20trip%3Aimdb&format=json

    HF !
'''


import sys
import requests
import os
import urllib
from bs4 import BeautifulSoup
#do a pip install PyExecJS
#import execjs


# -*- coding: utf-8 -*-
import scrapy


class SpiderDuck(scrapy.Spider):
    name = "SpiderDuck"

    def makeRequest(self, url):
        #assert type(url) is str
        return scrapy.Request(url, self.parse)

    def parse(self, response):

        for link in response.xpath("result__a").extract():
            item = dict()
            item['url'] = link.xpath("@href"),extract_first()
            yield item


movieName = "Harry Potter"
movieName.replace(" ", "%20")
url = "http://duckduckgo.com/?q="+movieName+" %3Aimdb"


sp = SpiderDuck()
links = sp.makeRequest(url)

print(links)

"""
def spider(url):
    page = urllib.request(url)
    #source_code = requests.get(url)
    #plain_text = source_code.text
    convert_data = BeautifulSoup(page)

    print(convert_data)
"""

"""
from bs4 import BeautifulSoup
import requests
import sys
class googleIt:
    def getMovie(self, movieName):
        movieName.replace(" ", "%20")
        url = "http://duckduckgo.com/?q="+movieName+" %3Aimdb"

        src = requests.get(url)
        plain = src.text

        soup = BeautifulSoup(plainSrc)

        print(soup)

        #for link in soup.findAll("a", {'class': 'result__a'}):
        for link in soup.findAll("a"):
            print("hey !")
            print(link)
            #print(title)


crawler = googleIt()
crawler.getMovie("Harry potter")
"""
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

'''
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
'''
