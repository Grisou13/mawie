# Mais Jamie, c'est quoi l'explorer ?

[![THEME SONG](http://img.youtube.com/vi/v4IC7qaNr7I/0.jpg)](http://www.youtube.com/watch?v=v4IC7qaNr7I)

# explorer

## explorer Class
The class explorer has the "public" method __parse()__ to parse the given folder.
Basically the function does :
1. Loop through the given folder  
2. Get every video file with the mime type  
3. Parse the file name  
4. Try to get the IMDB ID with the movie name  
5. If found, stores the __file__ information's (if not already stored)  
6. Get the info about the movie    
7. Stores the __movie__ information's if not already done !

```
>>> explorer = Explorer()
>>> found, notfound = explorer.parse(path_to_folder)
```

The two elements returned are dictionnaries which contains respecitely the found and the not found files.

### file parsing
We first used the [PTN library](https://github.com/divijbindlish/parse-torrent-name) to parse the files names.
Unfortunately, the library sometimes has a lack of precisions which cause some troubles.
So we added it to another library, [Guessit](https://github.com/guessit-io/guessit), to assert the parsing

```
>>> # with PTN lib
>>> parsed = PTN.parse("La.Vie.D.Adele.2013.FRENCH.BRRip.AC3.XviD-2T")
>>> print(parsed)
{'title': 'La Vie D Adele', 'group': '2T', 'codec': 'XviD', 'language': 'FRENCH', 'year': 2013, 'quality': 'BRRip', 'audio': 'AC3'}
>>> # with guessit
>>> parsed = guessit("La.Vie.D.Adele.2013.FRENCH.BRRip.AC3.XviD-2T")
>>> print(parsed)
MatchesDict([('title', 'La Vie D Adele'), ('year', 2013), ('language', <Language [fr]>), ('format', 'BluRay'), ('audio_codec', 'AC3'), ('video_codec', 'XviD'), ('release_group', '2T'), ('type', 'movie')])
>>> # and if we mix up both
>>> parsed = PTN.parse("La.Vie.D.Adele.2013.FRENCH.BRRip.AC3.XviD-2T")
>>> secondParsed = guessit("La.Vie.D.Adele.2013.FRENCH.BRRip.AC3.XviD-2T", {"T": parsed["title"]})
>>> pritn(secondParsed)
MatchesDict([('title', 'La Vie D Adele'), ('year', 2013), ('language', <Language [fr]>), ('format', 'BluRay'), ('audio_codec', 'AC3'), ('video_codec', 'XviD'), ('release_group', '2T'), ('type', 'movie')])
```

### Storage
The "File" and "Movie" can be a little bit fuzzy to discern yet.
A file is the phsyical element that we want to store.

__File Data Model__:

File  | &nbsp
------------- | -------------
path  | string
base  | string
movie.id | foreignKey movie.id
movie | relation to Movie
created_at | datetime

The model can be found at *app/models/File.py*

__Movie data model__:
And a movie is simple all the informations about a movie on imdb.
Movie  | &nbsp  
------------- | -------------
name  | string
imdb_id  | string
genre | string
desc | string
release | date
runtime  | string
actors  | string
directors  | string
writer  | string
poster  | string
rate  | string
files  | relation to File
viewed  | boolean

The model can be found at *app/models/Movie.py*


## googleIt Class
The class is mostly used by the explorer. 
There's two "public" functions that can be used :
The first one , __getMovieID()__, is to get a movie id with a title
```
>>> googleItPutain = googleIt()
>>> res = googleItPutain.getMovieID(MovieTitle="La guerre des étoiles")
>>> print(res)
"tt0076759"
```

And the second method, __getMovieInfo()__, is used for getting a movie object containing informations about the movie (plot, release date, actors, etc...)
```
>>> googleItPutain = googleIt()
>>> # works with movie ID
>>> r = googleItPutain.getMovieInfo(movieId = "tt0137523")
>>> # with a title (return a generator of movies found)
>>> r = googleItPutain.getMovieInfo(movieTitle = "Fight Club")
>>> # or finally with both movieID and movieTitle 
>>> # note that giving both parameters takes more time as we loop through the generator.
>>> r = googleItPutain.getMovieInfo(movieId = "tt0137523", movieTitle = "Fight CLUB")
>>> print(r.title)
"Fight Club"
>>> print(r.plots)
"Don't speak about it"
>>> print(r.release_date)
"1990-10-15"
```

### imdb api
To get the movies informations, we use the [IMDB api](https://app.imdb.com). 
To use the api easily we use the library [imdb-pie](https://github.com/richardasaurus/imdb-pie).

```
>>> from imdbpie import Imdb
>>> imdb = Imdb()
>>> title = imdb.get_title_by_id("tt0330373") # Harry Potter 4
>>> print(title.title)
"Harry Potter and the Goblet of Fire"
```

### duckduckGo research
To get all the information about a movie we need its ID.
To get the ID of a movie using its name (in any language), we do a request on duckduckgo.com that we parse using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/).
```
>>> import urllib.request
>>> from bs4 import BeautifulSoup
>>> term = "https://duckduckgo.com/html/?q=Harry Potter 4 :imdb"
>>> fp = urllib.request.urlopen(term)
>>> r = fp.read().decode("utf8")
>>> fp.close()
>>> soup = BeautifulSoup(r, "html.parser")
>>> print(soup.find_all("a", attrs={"class": u"result__a"}, href=True))
[<a class="result__a" href="http://www.imdb.com/title/tt0330373/" rel="nofollow"><b>Harry</b>]....
```


