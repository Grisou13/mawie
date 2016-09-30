import tkinter
from app.models.Movie import Movie

class Test():


    def __init__(self,root,movieFrame):
        movie = Movie()
        movie.name = "A Walk Through H: The Reincarnation of an Ornithologist"
        movie.imdb_id = "allo"
        movie.genre = "allo"
        movie.desc = "lorem sdfasdf asdf asdf"
        movie.release = "1979"
        movie.runtime = "allo"
        movie.actors = "allo"
        movie.directors = "allo"
        movie.writer = "allo"
        movie.poster = "http://ia.media-imdb.com/images/M/MV5BMTk5NTM2ODUwMF5BMl5BanBnXkFtZTcwNTI0OTgyMQ@@._V1_SX300.jpg"
        movieFrame.update(movie)
