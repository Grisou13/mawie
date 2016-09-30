import tkinter
from app.gui.components.movie_frame import MovieFrame
from app.models.Movie import Movie

class Gui():
    def __init__(self):
        root = tkinter.Tk()
        movieFrame= MovieFrame(root)
        movie = Movie()
        movie.name = "A Walk Through H: The Reincarnation of an Ornithologist"
        movie.imdb_id = "124135"
        movie.genre = "Rape"
        movie.desc = "lorem sfsadfs fsad fsadf sadf asfsad fas fasd fdas fdas fdas fdas fdasf dasf das fdas fdas fdasf sdfsdifsj kls fsdjklfjsklfj sfssdf asf dasf das fdas fjdfk jsflkjsimf3lkjklsjfsd"
        movie.release = "1979"
        movie.runtime = "1:30"
        movie.actors = "Brad Double u pitt"
        movie.directors = "Steven Alpichberg"
        movie.writer = "Steven Hawkins"
        #movie.poster = "http://ia.media-imdb.com/images/M/MV5BNjQ5NjEyMjU1OF5BMl5BanBnXkFtZTcwNDQ2NzI5NA@@._V1_SX300.jpg"
        movie.poster = '/../filmImg2.jpg' #be aware, need / before path
        movieFrame.updateMovie(movie)
        root.mainloop()
if __name__ == '__main__':
     gui = Gui()