import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
from urllib import request,error
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
        self.size = 350, 350
        sizeFontInfoFilm=11
        lengthMaxLbl=500
        padxLblInfo=250

        #Create widgets
        img = self.importPosterFilm()
        img.thumbnail(self.size)
        self.tk_img = ImageTk.PhotoImage(img)
        self.lblImgFilm = ttk.Label(self, image=self.tk_img)

        self.lblTitle = ttk.Label(self,font=("Arial",20),text="Aucun film sélectionné")
        self.lblScenarist = ttk.Label(self, text="Scenarist: -", wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblDirector = ttk.Label(self, text="Réalisateur -", wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblActor = ttk.Label(self, text="Acteurs: -", wraplength=lengthMaxLbl, font=("Arial", sizeFontInfoFilm))
        self.lblRuntime = ttk.Label(self, text="Durée: -", wraplength=lengthMaxLbl, font=("Arial", sizeFontInfoFilm))
        self.lblRate = ttk.Label(self, text="Note: -", wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblReleasedDate = ttk.Label(self, text="Date de sortie: -", wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblAwards = ttk.Label(self, text="Récompenses: -", wraplength=lengthMaxLbl, font=("Arial",sizeFontInfoFilm))
        self.lblCountry = ttk.Label(self, wraplength=lengthMaxLbl, text="Pays: -", font=("Arial",sizeFontInfoFilm))
        self.lblPlot = ttk.Label(self, wraplength="800",font=("Arial",sizeFontInfoFilm),text="Sysnopsis: -")
        self.lblLien = ttk.Label(self,text="Fichier(s) du film")

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
        self.lblTitle.config(text=movie.name)

        #poster
        img = self.importPosterFilm(movie.poster)
        img.thumbnail(self.size)
        self.tk_img = ImageTk.PhotoImage(img)
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

        sizeFontInfoFilm = 11
        list = ["C:\\generate_table.sql","C:\\users\\documents","c:\\SUSClientID.log"]
        if len(list)>1:
            self.lstBoxFiles = tkinter.Listbox(self, width=100, font=("Arial", sizeFontInfoFilm))
            self.lstBoxFiles.grid(row=11)
            for idx, film in enumerate(list):
                self.lstBoxFiles.insert(tkinter.END, film)
            ttk.Button(text="Voir film", width=100, command=self.openDirectory ).grid()


    #import the poster of the film, can be a local path or a url
    def importPosterFilm(self,path=''):
        try:
            html= request.urlopen(path)
            print(html)
            file = BytesIO(html.read())
        except ValueError:  # local path
            if  os.path.isfile(os.path.dirname(__file__)+path):
                file = os.path.dirname(__file__)+path
                print("file exists")
            else :
                print(os.path.dirname(__file__)+path)
                print("file doesn't exist")
                file = os.path.dirname(__file__)+'\..\..\..\.cache\\noPoster.jpg'
        image = Image.open(file)
        return image
    def openDirectory(self):
        path = self.lstBoxFiles.get(self.lstBoxFiles.curselection())
        if os.path.isfile(path):
            subprocess.Popen(r'explorer /select,"'+path+'"')
        else:
            print(path +"<- doesn't exist")
            return False