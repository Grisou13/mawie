from tkinter.ttk import Widget
import tkinter
import tkinter.ttk

from sqlalchemy import desc
import itertools

from app.models import db
from app.models.Movie import Movie
from app.research.research import Research
import types
from app.gui.components import GuiComponent

class AutocompleteCombobox(tkinter.ttk.Entry):
    def __init__(self, *arg, **kwargs):

        """

        :param arg:
        :param kwargs:
        """
        self.r = Research()
        if "match_func" in kwargs:
            self.matchFunc = kwargs["match_func"]
            del kwargs["match_func"]
        else:
            self.matchFunc = self.match
        if "autocomplete" in kwargs:
            self._autocomplete = kwargs["autocomplete"]
            del kwargs["autocomplete"]
        if "autocomplete_list" in kwargs:
            self._autocompleteList = kwargs["autocomplete_list"]
            del kwargs["autocomplete_list"]
        super(AutocompleteCombobox, self).__init__(*arg, **kwargs)



    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""

        self._completion_list = completion_list  # Work with a sorted list

        # self._elements = [] if isinstance(completion_list,types.GeneratorType) else completion_list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self.bind('<Return>', (lambda e: print(e)))
        #self['values'] = [] if isinstance(completion_list,
        #                                  types.GeneratorType) else completion_list  # Setup our popup menu

    @staticmethod
    def match(value, inputValue):
        if isinstance(value, db.Model):
            return str(value).lower().startswith(inputValue.lower())
        return value.lower().startswith(inputValue.lower())

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        # reset the completion list to the selected value
        self._completion_list = self.r.search(self.get())
        self._autocompleteList(self._completion_list)
        # make them visible in the combo dropdown

        # self['values'] = [self.get()] + first
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tkinter.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if self.matchFunc(element, self.get()):  # Match case insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tkinter.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tkinter.END)
            #self.onAutocompleteFunc(self._hits[self._hit_index])
            print(self.position)
            print(self._hit_index)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tkinter.INSERT), tkinter.END)
            self.position = self.index(tkinter.END)
        if event.keysym == "Left":
            if self.position < self.index(tkinter.END):  # delete the selection
                self.delete(self.position, tkinter.END)
            else:
                self.position = self.position - 1  # delete one character
                # self.delete(self.position, tkinter.END)
        if event.keysym == "Right" or event.keysym == "Return":
            self.position = self.index(tkinter.END)  # go to end (no selection)
            self._autocomplete(self._hits[self._hit_index])
        if len(event.keysym) == 1:
            self.autocomplete()
            # No need for up/down, we'll jump to the popup
            # list at the position of the autocompletion


class SearchWidget(AutocompleteCombobox):
    pass


# must complete with the research autocomplete
class SearchListWidget(tkinter.Listbox):
    pass


class SearchFrame(tkinter.Frame, GuiComponent):
    def __init__(self, gui, *arg, **kwargs):
        self.gui = gui
        self.gui.register_listener(self)
        super(SearchFrame, self).__init__(gui.root_tkinter, *arg, **kwargs)
        self.grid()
        self.search_bar = SearchWidget(self, autocomplete=self.onAutoComplete, autocomplete_list=self.onList)
        self.search_bar.set_completion_list([])
        self.search_bar.focus_set()
        self.search_bar.grid()


        #self.result_list = SearchListWidget(self)
        #self.result_list.grid()
        self.grid()
        #self.result_list.focus_set()
    def onList(self,gen):

        self.gui.dispatchAction("search_list",gen)
        self.result_list.delete(0, tkinter.END)
        for i in gen:
            self.result_list.insert(tkinter.END, str(i))

        self.gui.dispatchAction("list_result_search",gen)
        #self.result_list.delete(0, tkinter.END)
        #for i in gen:
        #    self.result_list.insert(tkinter.END, str(i))

    def onAutoComplete(self,i):
        self.result_list.delete(0, tkinter.END )
        self.result_list.insert(tkinter.END,str(i))
        self.gui.dispatchAction("search_selected",i)
    def handleAction(self,name,data):
        pass
    def requestAction(self,name):
        pass
if __name__ == '__main__':
    from app.gui.gui import Gui
    g = Gui.instance()
    g.start()
    """root = tkinter.Tk(className=' AutocompleteEntry demo')
    root.minsize(400, 400)


    def on_field_change(index, value, op):
        print("combobox updated to ", s.get())


    v = tkinter.StringVar()
    v.trace('w', on_field_change)
    s = SearchWidget(root, textvar=v)
    l = [m.name for m in Movie.query(Movie.name).order_by(desc(Movie.created_at)).limit(5).all()]
    s.set_completion_list([])  # get the last 5 moviews
    s.pack()
    s.focus_set()
    root.mainloop()"""

    # TODO
    """
    I have an idea
    Use combobox list to get the item index
    Get the generator till index
    Gets the movie element and runs the MovieFrame component with the movie
    """
"""
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

"""