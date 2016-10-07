from tkinter.ttk import Widget
import tkinter
import tkinter.ttk

from sqlalchemy import desc
import itertools

from app.models import db
from app.models.Movie import Movie
from app.research.research import  Research

class AutocompleteCombobox(tkinter.ttk.Combobox):
    def __init__(self, *arg, **kwargs):
        super(AutocompleteCombobox, self).__init__(*arg, **kwargs)
        self.r = Research()

    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""

        self._completion_list = completion_list  # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu
    @staticmethod
    def match(value,inputValue):
        if isinstance(value,db.Model):
            return str(value).lower().startswith(inputValue.lower())
        return value.lower().startswith(inputValue.lower())
    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        # reset the completion list to the selected value
        self._completion_list = self.r.search(self.get())
        # make them visible in the combo dropdown
        first = [x for _, x in zip(range(3), self._completion_list)]
        self['values'] = [self.get()] + first
        print(self['values'])
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tkinter.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if self.match(element,self.get()):  # Match case insensitively
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
                self.delete(self.position, tkinter.END)
        if event.keysym == "Right":
            self.position = self.index(tkinter.END)  # go to end (no selection)
        if len(event.keysym) == 1:
            self.autocomplete()
            # No need for up/down, we'll jump to the popup
            # list at the position of the autocompletion

class SearchWidget(AutocompleteCombobox):
    pass
#must complete with the research autocomplete
class SearchListWidget(tkinter.Listbox):
    pass
if __name__ == '__main__':
    root = tkinter.Tk(className=' AutocompleteEntry demo')
    root.minsize(400,400)


    def on_field_change(index, value, op):
        print("combobox updated to ", s.get())
    v = tkinter.StringVar()
    v.trace('w', on_field_change)
    s = SearchWidget(root, textvar=v)
    l = [m.name for m in Movie.query(Movie.name).order_by(desc(Movie.created_at)).limit(5).all()]
    s.set_completion_list([]) # get the last 5 moviews
    s.pack()
    s.focus_set()
    root.mainloop()

    #TODO
    """
    I have an idea
    Use combobox list to get the item index
    Get the generator till index
    Gets the movie element and runs the MovieFrame component with the movie
    """