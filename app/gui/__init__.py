from app.gui.gui import Gui
from app.gui.movie_frame import MovieInfo

def run():
    g = Gui()
    movieInfo={'director': "Steven Spielberg",
               'scenarist': "Good Kill",
               'title': "Good Kill",
               'actor': "Frank Dubosk, Brad Pitt",
               'rate': "7/10",
               'image': "filmImg.jpg",
               'awards': "Best film 2015",
               'country': "USA, Afghanistan",
               'releaseDate': "02.10.2014",
               'plot': "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt \n ut labore et dolore magna aliqua. Ut enim ad minim veniam,quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodoconsequat. Duis aute irure dolor in reprehenderit in voluptate velit essecillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat nonproident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
               }
    m = MovieInfo(g.root,movieInfo)
    g.root.mainloop()
if __name__ == '__main__':
    #run()
    pass

