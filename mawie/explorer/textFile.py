import os
import re
import urllib.request
from mimetypes import MimeTypes

from google import google

import sys
from guessit import guessit
import libs.PTN as PTN
from mawie.explorer.googleit import googleIt


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

def hopeless(files):
    g = googleIt()
    for f in files:
        k = g.getMovieInfo(movieTitle=f["title"])
        print("a new one !")
        for j in k:
            print("same")
            print(j.title)


if __name__ == "__main__":
    files = parseFolder("../../stubs/FILM_a_trier/")

    hopeless(files)

    #print(k)
