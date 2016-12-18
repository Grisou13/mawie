#Database
To have a portable application, we used SQLite. You can find the file of the database in `.cache/main.sqlite`
To access our data we chose to use [Active-Alchemy GitHub](https://github.com/mardix/active-alchemy) as ORM which is a 
wrapper around [SQLAlchemy](http://www.sqlalchemy.org/) 



## Database Structure
Our database is composed of two table : Movie and File.
The "File" and "Movie" can be a little bit fuzzy to discern yet.
A file is the physical element that we want to store and a movie is simply the information about a movie on IMDb. 
This way, you can have several files of a same movie. This way, if you have 2 files (one file in version original and 
one file in french for example) of the movie  "Harry Potter and the Philosopher's Stone",They are all linked to the same
movie record in the movie table.


__File Data Model__:

File  | Data type|
------| --------|
path  | string
base  | string
movie.id | foreignKey movie.id
movie | relation to Movie
created_at | datetime

The model can be found at `app/models/File.py`

__Movie data model__:
Movie  | Data type 
----- | -------------
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

The model can be found at `app/models/Movie.py`

### Some examples how to fetch data
#### Get a Movie or a File
if you want to get specific a movie or file, import the model then use `<Model_Name>.get(<id_of_the_movie>)`
for example, if you to get the movie which has the ID 1 and print its title.

```Python
from mawie.models.Movie import Movie

aMovie = Movie.get(1)
print(aMovie.name)
```
#### Delete a file or movie
aMovie.delete()

#### Store a file
#### Store a movie


