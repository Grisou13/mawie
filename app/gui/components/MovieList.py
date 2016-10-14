import tkinter



class MovieListFrame(tkinter.Frame):
    def __init__(self,root):
        tkinter.Frame.__init__(self,root)
        self.grid(column=1,row=0,rowspan=2)
        self.createWidget()

    def createWidget(self):
        bgFrame = "#1E1E1F"
        colorFont = "#CBC9CF"
        btnColor = "#191919"
        lstColor="#191919"
        lstSelectColor="#39393B"
        sizeFontInfoFilm = 11
        lengthMaxLbl = 500
        self.scrollBarLstBoxFilms = tkinter.Scrollbar(self)
        self.config(bg=bgFrame)

        self.lblListFilms = tkinter.Label(text="Liste des films répertoriés",bg=bgFrame, fg=colorFont)
        self.lstFilms= tkinter.Listbox(self, width=50, bg=lstColor, fg=colorFont, selectbackground=lstSelectColor, activestyle="none",
                        font=("Arial", sizeFontInfoFilm), yscrollcommand=self.scrollBarLstBoxFilms.set)
        self.btnSelection=tkinter.Button(text="Voir les informations du film", state=tkinter.DISABLED)

        self.lblListFilms.grid(column=0,row=0)
        self.lstFilms.grid(column=0,row=1)
        self.scrollBarLstBoxFilms.grid()


    def updateWidget(self,movies):
        self.lstFilms.delete(0)
        for movie in movies:
            self.lstFilms.insert(movie.name)
        if len(movies) >0:
            self.btnSelection.config(state=tkinter.NORMAL)
        else:
            self.btnSelection.config(state=tkinter.DISABLED)


