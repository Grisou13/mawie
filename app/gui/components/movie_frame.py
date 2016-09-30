import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
from urllib.request import *
from io import BytesIO
import subprocess
import os

class MovieFrame(tkinter.Frame):
    def __init__(self,root):
        super(MovieFrame, self).__init__(root)
        self.grid()
        self.columnconfigure(0,weight=0)
        self.createWidget(self)

    def createWidget(self,frame):
        sizeFontInfoFilm=11
        lengthMaxLbl=500
        padxLblInfo=250

        #Create widgets
        self.tk_img = None
        self.lblImgFilm = ttk.Label(self, image=self.tk_img)
        self.lblTitle = ttk.Label(self,font=("Arial",20))
        self.lblScenarist = ttk.Label(self, text="Scenarist: ", wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblDirector = ttk.Label(self, text="real", wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblActor = ttk.Label(self, text="auteur", wraplength=lengthMaxLbl, font=("Arial", sizeFontInfoFilm))
        self.lblRuntime = ttk.Label(self, text="runTime", wraplength=lengthMaxLbl, font=("Arial", sizeFontInfoFilm))
        self.lblRate = ttk.Label(self, text="auteur", wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblReleasedDate = ttk.Label(self, text="auteur", wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblAwards = ttk.Label(self, text="auteur", wraplength=lengthMaxLbl, font=("Arial",sizeFontInfoFilm))
        self.lblCountry = ttk.Label(self, wraplength=lengthMaxLbl, text="auteur", font=("Arial",sizeFontInfoFilm))
        self.lblPlot = ttk.Label(self, wraplength="800",font=("Arial",sizeFontInfoFilm))

        ''' ***** V1
         elf.lblImgFilm.grid(row=1, column=0, rowspan=7)         self.lblScenarist.grid(row=1, column=1, sticky="W")
         self.lblDirector.grid(row=2, column=1, sticky="W")
         self.lblActor.grid(row=3, column=1,sticky="W")
         self.lblRate.grid(row=4, column=1, sticky="W")
         self.lblAwards.grid(row=6, column=1, sticky="W")
         self.lblCountry.grid(row=7, column=1, sticky="W")
         self.lblReleasedDate.grid(row=5, column=1, sticky="W")
         self.lblPlot.grid( row=8, column=0, columnspan=2,sticky="W")'''

        #place widgets
        self.lblTitle.grid(row=0, column=0, columnspan=3, sticky="W", padx=4)
        self.lblImgFilm.grid(row=1, column=0,rowspan=9, sticky="W")
        self.lblScenarist.grid(row=1, column=0,sticky="W", padx=(padxLblInfo,0))
        self.lblDirector.grid(row=2, column=0,sticky="W", padx=(padxLblInfo,0))
        self.lblActor.grid(row=3, column=0,sticky="W", padx=(padxLblInfo,0))
        self.lblRuntime.grid(row=4, column=0, sticky="W", padx=(padxLblInfo, 0))
        self.lblRate.grid(row=5, column=0,sticky="W", padx=(padxLblInfo,0))
        self.lblAwards.grid(row=7, column=0,sticky="W",padx=(padxLblInfo,0))
        self.lblCountry.grid(row=8, column=0, sticky="W", padx=(padxLblInfo,0))
        self.lblReleasedDate.grid(row=9, column=0, sticky="W", padx=(padxLblInfo,0))
        self.lblPlot.grid(row=10, column=0, columnspan=2, stick="W", pady=2)

    #display/change movie info
    def updateMovie(self,movie):
        self.size = 350, 350

        self.lblTitle.config(text=movie.name)

        #poster
        self.img = self.importPosterFilm('http://ia.media-imdb.com/images/M/MV5BNjQ5NjEyMjU1OF5BMl5BanBnXkFtZTcwNDQ2NzI5NA@@._V1_SX300.jpg')
        self.img.thumbnail(self.size)
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.lblImgFilm.config(image=self.tk_img)

        #info movie
        self.lblTitle.config(text=movie.name)
        self.lblScenarist.config(text="Scénariste: "+movie.writer)
        self.lblDirector.config(text="Réalisateur: "+movie.directors)
        self.lblActor.config(text="Acteur: "+movie.actors)
        #self.lblRate.config(text="Note: "+movie.rate)
        #self.lblAwards.config(text="Récompense: "+movie.)
        #self.lblCountry.config(text="Pays: "+movie.)
        self.lblReleasedDate.config(text="Date de sortie: "+movie.release)
        self.lblPlot.config(text="Synopsis: "+movie.desc)

        #create button to open file
        list = ["C:\\Users\Ilias\\PycharmProjects\\appScrapy\\appScrapy\\apiFilm","C:\\Users\Ilias\\documents","C:\\Users\Ilias\\documents"]
        listFilmsPath =[]
        row = 11
        for idx, film in enumerate(list):
            width = 15
            padx=200
            listFilmsPath.append(ttk.Button(text="Voir film",width=width, command=lambda film=film: self.openDirectory(film)))
            listFilmsPath[idx].grid(row=row,padx=(200,idx*padx))
            print(str(idx*width))

    #import the poster of the film, can be a local path or a url
    def importPosterFilm(self,path):
        try:
            html=urlopen(path)
            file = BytesIO(html.read())
        except ValueError:  # local path
            if  os.path.isfile(path):
                file = open(path)
            else:
                print("can't import poster")
                return False
        image = Image.open(file)
        return image

    def openDirectory(self,path):
        if os.path.isdir(path):
            subprocess.Popen(r'explorer /select,"'+path+'"')
        else:
            print(path +"<- doesn't exist")
            return False