import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess


class MovieInfo():


    def __init__(self,root,movieInfo):
        self.frameMovie = tkinter.Frame(root)
        self.frameMovie.grid()
        self.frameMovie.columnconfigure(0,weight=0)
        self.createWidget(self.frameMovie)
        self.update(movieInfo)

        #subprocess.Popen('explorer "C:"')


    def createWidget(self,frame):
        sizeFontInfoFilm=11
        lengthMaxLbl=500
        self.size = 300, 300

        self.var = tkinter.StringVar()
        self.img = Image.open("filmImg.jpg")
        self.img.thumbnail(self.size)
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.lblImgFilm = ttk.Label(frame, image=self.tk_img)

        self.lblTitle = ttk.Label(frame,font=("Arial",20))
        self.lblScenarist = ttk.Label(frame, textvariable=self.var, wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblDirector = ttk.Label(frame, text="real",  wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblActor = ttk.Label(frame, text="auteur",  wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblRate = ttk.Label(frame, text="auteur",  wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblReleasedDate = ttk.Label(frame, text="auteur",  wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblAwards = ttk.Label(frame, text="auteur",   wraplength=lengthMaxLbl,font=("Arial",sizeFontInfoFilm))
        self.lblCountry = ttk.Label(frame, wraplength=lengthMaxLbl,text="auteur",font=("Arial",sizeFontInfoFilm))
        self.lblPlot = ttk.Label(frame, wraplength="800",font=("Arial",sizeFontInfoFilm), text = "olo ala sdf sd fsadfsdf sadf asf asf as fas fjkkljkl akljf3fklajr 2 kjaf jasj fajf a asf asf asf afasfasf asf asf")

        self.lblTitle.grid(row=0, column=0,columnspan=3, sticky="W")
        self.lblImgFilm.grid(row=1, column=0, rowspan=7)

        ''' ***** V1
         self.lblScenarist.grid(row=1, column=1, sticky="W")
         self.lblDirector.grid(row=2, column=1, sticky="W")
         self.lblActor.grid(row=3, column=1,sticky="W")
         self.lblRate.grid(row=4, column=1, sticky="W")
         self.lblAwards.grid(row=6, column=1, sticky="W")
         self.lblCountry.grid(row=7, column=1, sticky="W")
         self.lblReleasedDate.grid(row=5, column=1, sticky="W")
         self.lblPlot.grid( row=8, column=0, columnspan=2,sticky="W")'''

        self.lblImgFilm.grid(row=1, column=0,rowspan=7, sticky="W")
        self.lblScenarist.grid(row=1, column=0,sticky="W", padx=(220,0))
        self.lblDirector.grid(row=2, column=0,sticky="W", padx=(220,0))
        self.lblActor.grid(row=3, column=0,sticky="W", padx=(220,0))
        self.lblRate.grid(row=4, column=0,sticky="W", padx=(220,0))
        self.lblAwards.grid(row=6, column=0,sticky="W",padx=(220,0))
        self.lblCountry.grid(row=7, column=0, sticky="W", padx=(220,0))
        self.lblReleasedDate.grid(row=5, column=0, sticky="W", padx=(220,0))
        self.lblPlot.grid(row=8, column=0, columnspan=2, stick="W")





    def update(self,movieInfo):
        self.img = Image.open(movieInfo["image"])
        self.img.thumbnail(self.size)
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.lblTitle.config(text=movieInfo["title"])
        self.lblScenarist.config(text="Scénariste: "+movieInfo["scenarist"])
        self.lblDirector.config(text="Réalisateur: "+movieInfo["director"])
        self.lblActor.config(text="Acteur: "+movieInfo["actor"])
        self.lblRate.config(text="Note: "+movieInfo["rate"])
        self.lblAwards.config(text="Récompense: "+movieInfo["awards"])
        self.lblCountry.config(text="Pays: "+movieInfo["country"])
        self.lblReleasedDate.config(text="Date de sortie: "+movieInfo["releaseDate"])
        self.lblPlot.config(text="Synopsis: "+movieInfo["plot"])
        self.lblImgFilm.config(image=self.tk_img)
