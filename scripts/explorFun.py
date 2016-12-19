import os
import re
import inspect
import time
import urllib.request
from mimetypes import MimeTypes

import sys
from guessit import guessit
import itertools

from pws import Google
from pws import Bing
import requests
from bs4 import BeautifulSoup


#cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
#if cmd_folder not in sys.path:
#    sys.path.insert(0, cmd_folder)

if __name__ == '__main__':
    sys.path.append(os.path.join(os.getcwd(), "../../"))

import libs.PTN as PTN
from mawie.explorer.googleit import GoogleIt


def isAVideo(path):
    # we get the mime type
    mime = MimeTypes().guess_type(urllib.request.pathname2url(path))
    # if not recognised , be a array (None, None)
    if all(v is None for v in mime):
        return False
    # and finally check if it is a video in array ex: (video, avi)
    return "video" in mime[0]


def parseName(movieName):
    mov = PTN.parse(re.sub(r'avi', "", movieName.replace(".", " ")))
    g = guessit(movieName, {"T": mov["title"]})
    return g

def parseFile(filePath):
    path, filename = os.path.split(filePath)
    parsed = parseName(filename)

    parsed["filePath"] = filePath
    return parsed

def parseFolder(path):
    path = os.path.realpath(path)

    files = []
    for r, dirs, _files in os.walk(path, topdown=False):
        for f in _files:
            path = os.path.join(r, f)
            if isAVideo(path):
                # we parse the files here
                files.append(parseFile(path))

                # for d in dirs:
                #     # as Thomas said : Recursion bitch
                #     files.extend(self.getMoviesFromPath(os.path.join(r,d)))

    return files

def getInfos(files):
    for f in files:
        res = google.search(f["title"] + " :imdb")
        print(res.link)
    return files

class GenLen:
    def __init__(self, gen, len):
        self.gen = gen
        self.len = len
    def __len__(self):
        return self.len
    def __iter__(self):
        return self.gen

def f(files):
    g = GoogleIt()
    lastTitle = ""
    lastId = ""
    for f in files:
        time.sleep(1)
        if f["title"] != lastTitle:
            imdbId = g.getMovieID(f["title"])
            lastTitle = f["title"]
            lastId = imdbId
        else:
            imdbId = lastId

        if not imdbId:
            print("we give it a second try btw..")
            print(g.getMovieID(f["title"], secondTry = True))

        print(imdbId)

def s(rr):
    #http://www.bing.com/search?q=hello+world&first=9
    term = "http://www.bing.com/search?q="+rr+" :imdb"
    h = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"

    res = requests.get(term, headers={"user-agent":h})

    r = BeautifulSoup(res.text, "html.parser").find_all('li', attrs = {'class' : 'b_algo'})

    for prout in r:
        print("")
        print(prout.find("a").get("href"))




def hopeless(files):
    g = GoogleIt()
    for f in files:
        #print("title is :")
        #print(f["title"])

        k = g.getMovieInfo(movieTitle=f["title"])
        h = GenLen(k, 1)

        if f["title"] == "E T LExtra Terrestre":
            print("found  extra Terrestre")
            print(len(h))
            for kk in k:
                print(k)
                print(dir(k))


        #print(len(h))
        #print(list(h))


if __name__ == "__main__":
    files = parseFolder("../../stubs/FILM_a_trier/")
    f(files)

    #print(k)
