import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk
from urllib import request
from io import BytesIO
import os

from app.gui.components import GuiComponent


class MovieFrame(tkinter.Frame, GuiComponent):
    def __init__(self, parent, gui, *arg, **kwargs):
        self.gui =gui
        gui.register_listener(self)
        super(MovieFrame, self).__init__(parent)

        self.grid(column=0,row=1)
        self.columnconfigure(0,weight=0)
        self.createWidget()


    def createWidget(self):
        self.flagLstBoxDisplayed = False
        self.size = 400,400
        bgFrame = "#1E1E1F"
        colorFont = "#CBC9CF"
        btnColor = "#191919"
        lstColor="#191919"
        lstSelectColor="#39393B"

        self.scrollBarLstBoxH = tkinter.Scrollbar(self, orient=tkinter.HORIZONTAL)
        scrollBarLstBoxV = tkinter.Scrollbar(self,orient=tkinter.VERTICAL)

        sizeFontInfoFilm=11
        lengthMaxLbl=500
        padxLblInfo=300

        self.config(bg=bgFrame)

        #Create widgets
        img = self.importPosterFilm()
        img.thumbnail(self.size)
        self.tk_img = ImageTk.PhotoImage(img)
        self.lblImgFilm = tkinter.Label(self, image=self.tk_img)

        self.lblTitle = tkinter.Label(self,bg=bgFrame,fg=colorFont,font=("Arial",20),
                                      text="Aucun film sélectionné")
        self.lblScenarist = tkinter.Label(self, text="Scenarist: -", wraplength=lengthMaxLbl,
                                          bg=bgFrame,fg=colorFont,font=("Arial",sizeFontInfoFilm))
        self.lblDirector = tkinter.Label(self, text="Réalisateur -", wraplength=lengthMaxLbl,
                                         bg=bgFrame,fg=colorFont,font=("Arial",sizeFontInfoFilm))
        self.lblActor = tkinter.Label(self, text="Acteurs: -", wraplength=lengthMaxLbl,
                                      bg=bgFrame,fg=colorFont, font=("Arial", sizeFontInfoFilm))
        self.lblRuntime = tkinter.Label(self, text="Durée: -", wraplength=lengthMaxLbl,
                                        bg=bgFrame,fg=colorFont, font=("Arial", sizeFontInfoFilm))
        self.lblRate = tkinter.Label(self, text="Note: -", wraplength=lengthMaxLbl,
                                     bg=bgFrame,fg=colorFont,font=("Arial",sizeFontInfoFilm))
        self.lblReleasedDate = tkinter.Label(self, text="Date de sortie: -", wraplength=lengthMaxLbl,
                                             bg=bgFrame,fg=colorFont,font=("Arial",sizeFontInfoFilm))
        self.lblAwards = tkinter.Label(self, text="Récompenses: -", wraplength=lengthMaxLbl,
                                       bg=bgFrame,fg=colorFont, font=("Arial",sizeFontInfoFilm))
        self.lblCountry = tkinter.Label(self, wraplength=lengthMaxLbl, text="Pays: -",bg=bgFrame,
                                        fg=colorFont, font=("Arial",sizeFontInfoFilm))
        self.lblPlot = tkinter.Label(self, wraplength="800",bg=bgFrame,fg=colorFont,
                                     justify=tkinter.LEFT,font=("Arial",sizeFontInfoFilm),text="Sysnopsis: -")
        self.lstBoxFiles = tkinter.Listbox(self, width=100,bg=lstColor,fg=colorFont ,
                                           selectbackground=lstSelectColor, activestyle="none", font=("Arial", sizeFontInfoFilm),xscrollcommand=self.scrollBarLstBoxH.set)
        self.btnGotoFile = tkinter.Button(self,text="Voir film", width=50, bg=btnColor, fg=colorFont,
                                          font=("Arial",sizeFontInfoFilm),command=self.openDirectory)
        self.scrollBarLstBoxH.config(command=self.lstBoxFiles.xview,width=120,troughcolor=bgFrame)


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
        self.lblAwards.grid(row=6, column=0,sticky="W",padx=(padxLblInfo,0))
        self.lblCountry.grid(row=7, column=0, sticky="W", padx=(padxLblInfo,0))
        self.lblReleasedDate.grid(row=8, column=0, sticky="W", padx=(padxLblInfo,0))
        self.lblPlot.grid(row=10, column=0, columnspan=2, sticky="W", pady=4)
        self.btnGotoFile.grid(row=13,pady=4)

    #display/change movie info
    def updateMovie(self,movie):
        self.files = movie.files
        if self.flagLstBoxDisplayed is True:
            self.lstBoxFiles.grid()
            self.scrollBarLstBoxH.grid()
            self.flagLstBoxDisplayed = False
        self.lstBoxFiles.delete(0)
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

        if len(self.files)>1:
            self.lstBoxFiles.grid(row=11)
            self.scrollBarLstBoxH.grid(row=11,column=0, pady=(100,0),sticky=tkinter.W+tkinter.E+tkinter.N)
            for  file in self.files:
                self.lstBoxFiles.insert(tkinter.END, file.path)
            self.lstBoxFiles.select_set(0)
            self.lstBoxFiles.grid()
            self.flagLstBoxDisplayed = True

        print(len(self.files))
    #import the poster of the film, can be a local path or a url
    def importPosterFilm(self,path=''):
        flagNoPoster = True
        file = os.path.dirname(__file__) + '/../../../.cache//noPoster.jpg'
        try:
            html= request.urlopen(path)
            file = BytesIO(html.read())
            flagNoPoster=False
        except ValueError:  # local path
            if  os.path.isfile(os.path.dirname(__file__)+path):
                file = os.path.dirname(__file__)+path
                print("file exists")
                flagNoPoster =False
            else :
                print(os.path.dirname(__file__)+path)
                print("file doesn't exist")
        except request.URLError: #in case there isn't the internet or the url gives 404 error or bad url
            print("a problem with the connection or the url has occurred")
        if flagNoPoster is True:
            file = os.path.dirname(__file__) + '/../../../.cache//noPoster.jpg'
        image = Image.open(file)
        return image

    def openDirectory(self):
        if self.lstBoxFiles.size()>=1:
            path = self.lstBoxFiles.get(self.lstBoxFiles.curselection())
        else:
            path = self.files[0].path
        if os.path.isfile(path):
            os.startfile(path)
            #subprocess.Popen(r'explorer /select,"'+path+'"')
        else:
            print(path)
            messagebox.showerror("Fichier inexistant","Il semblerait que le fichier sélectionné ("+path+") n'existe plus")
    def handleAction(self,name,data):
        if name == 'update_movie_info':
            self.updateMovie(data)
    def requestAction(self,name):
        pass