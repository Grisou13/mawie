# GUI
At the beginning of the project, we chose to use Tkinter but we find a little bit incomplete for what we would  like to do
so, we decide to change to pyqt.

## Listing of frame
We chose to put a "Q" in the front of the filename of every graphical component. These components are all in the
directory ``` mawie.gui.components ```.
Actually there are XXX frames which are:

Filename | Class name | Description | Inherits|
---------|------------|-------------|---------|
QResearchWidget|QResearchWidget| This component communicates with ```mawie.research.search```  to launch research and then emit an event to QMovieListWidget to show results|
QAdvancedSearch|AdvancedSearch|display the form to do advanced research
QMovieWidget|MovieWidget| Display the info of the movie. it allows you to show you the movie file in your browser, play the movie in your default media player or in our customized media player, you can also delete the file associates to the movie|
QExplorer|AddFilesWidget| This component purpose is to add the folder you want the search movies files in and add it to the databases, in case a file can be parsed you can provide an IMDb url and it will get the info of the film|
QMovieListWidget|MovieListWidget| This widget displays the movies of a research|
QMoviePlayer| MoviePlayer| This is the player media player. The file format/codec it can read depend on the OS and codec you have. On Windows in depends on DirectShow; OSX depends on QuickTime Player and on Linux it depends  the installed Gstreamer plugins|
QError|ErrorWidget|Display error that we didn't catch|
QPoster|QPoster| This is a label that's enable to load movie poster asynchronously
QStackedWidget|ComponentArea|This is frame is where all the frames are stored.
QSettings|SettingsWidget| This frame is used to change the settings.

###MovieListWidget
#### Method updateWidgets(films)
argument films: a generator of objects model Movie
This method updates the list of films

#### Class ResultRow inherited QWidget
This class is the widget of a row in the MovieListWidget

###MovieWidget
#### Method updateWidgets(film)
argument film: a object model Movie
This method updates widgets with the information of the given film in argument

###SettingsWidget
The location where the settings are stored depend of your system:
Windows: HKEY_CURRENT_USER\Software\CPNV\MAWIE
MacOs: $HOME/Library/Preferences/com.CPNV.MAWIE.plist
Linux: $HOME/.config/CPNV/MAWIE.conf

####Settings available
CPNV->MAWIE->first launch
description: this is used to know if it's the first time the program is lauchned
default value : true
CPNV->MAWIE->infomovie->player-default
description: this allows to only use the default media player when you're in the MovieInfo and you clicked on "play film"
default value : true
CPNV->MAWIE->updator->updator-enabled
description: this setting enable/disable the updator
default value: true
CPNV->MAWIE->updator->frequency
description: if the updator is enabled this setting set the frequency the updator will execute its checking.
there are predefined values : 300,1800,6000 and 3600 (there are in milliseconds)
default value : 1800  


###ComponentArea
#### addWidget(widget)
This method is used to add a widget to the ComponentArea.


## How to add a widget
To create a graphical component, create a file in ```mawie.gui.components``` (the location has no effect but it's just to keep the structure of the project).
You have to inherits the class of your graphical component from GuiComponent which allows to receive event. 
```Python
from mawie.gui.components import GuiComponent

class MyWidget(QGuiComponent):
    def __init__(self,parent = None):
        super().__init__(parent)
```

Then, you have to add the method ```handle```. it will allow you to receive Event and do something with it
```Python
def handle(event):
    super().handle(event)
```
This is where you catch event and do something with it. for example :
```Python
def handle(event):
    super().handle(event)
    if isinstance(event,ResearchResponse):
        self.updateMyWidget(event.data)

```
## Events
### Listing of emit events
### How to create a event
To create a event, go to the event




### How to switch the frame
To switch frame you have to emit the Event ShowFrame(FrameYouWantToShow.__name__). if you want to pass data with it as a film
for example, you can do it this way : ShowFrame(FrameYouWantToShow.__name__, film)


```Python
#the widget where from you want to change frame

self.emit(ShowMyWidget)
```
```Python
#The widget you want to display

handle(event):
    if isinstance(event,ShowMyWidget):
        self.emit(ShowFrame(self))
    
```





