#GUI
At the beginning of the project, we chose to use Tkinter but we find a little bit incomplete for what we would to do
some we decide to change to pyqt.



##Listing of frame
We chose to put a "Q" in the front of the filename of every graphical component. These components are all in the
directory ``` mawie.gui.components ```.
Actually there are XXX frames which are:

Filename | Class name | Description | Inherits |
----------|-----------|------------|-------------
QResearchWidget|QResearchWidget| This component communicates with ```mawie.research.search```  to launch research and then emit an event to QMovieListWidget to show results
QAdvancedSearch|AdvancedSearch|display the form to do advanced research
QMovieWidget|MovieWidget| Display the info of the movie. it allows you to show you the movie file in your browser, play the movie in your default media player or in our customized media player, you can also delete the file associates to the movie
QExplorer|AddFilesWidget| This component purpose is to add the folder you want the search movies files in and add it to the databases, in case a file can be parsed you can provide an IMDb url and it will get the info of the film
QMovieListWidget|MovieListWidget| This widget displays the movies of a research
QMoviePlayer| MoviePlayer| This is the player media player. The file format/codec it can read depend on the OS and codec you have. On Windows in depends on DirectShow; OSX depends on QuickTime Player and on Linux it depends  the installed Gstreamer plugins
QError|ErrorWidget|Display error that we didn't catch
QPoster|QPoster| This is a label that's enable to load movie poster asynchronously 
QStackedWidget|ComponentArea|This is frame is where all the frames are stored.



##How to add a widget
To create a graphical component, create a file in ```mawie.gui.components``` (the location has no effect but it's just to keep the structure of the project).
You have to inherits the class of your graphical component from GuiComponent which allows to receive event. 
´´´
from mawie.gui.components import GuiComponent

class MyWidget(QGuiComponent):
    def __init__(self,parent = None):
        super().__init__(parent)
´´´

Then, you have to add the method ```handle```. 
```
    def handle(event):
        super().handle(event)
```
This is where you catch event and do something with it. for example:
```
	def handle(event):
        super().handle(event)
        if isinstance(event,ResearchResponse):
            self.updateMyWidget(event.data)

```
##Events
###Listing of emit events
###How to create one






###How to switch the frame


