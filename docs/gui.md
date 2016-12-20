# GUI
At the beginning of the project, we chose to use Tkinter but we find a little bit incomplete for what we would  like to do
so, we decide to change to pyqt. 

## QGui
## Listing of graphical componenet
We chose to put a "Q" in the front of the filename of every graphical component. These components are all in the
directory ``` mawie.gui.components ```.


| Filename         | Class name      | Description                                                                                                                                                                                                                          | Inherited from |
|------------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| QResearchWidget  | ResearchWidget  | This component communicates with ```mawie.research.search```,to launch research and then emit an event to QMovieListWidget to show results                                                                                           |                | 
| QAdvancedSearch  | AdvancedSearch  | display the form to do advanced research                                                                                                                                                                                             | Inherited from |
| QMovieWidget     | MovieWidget     | Display the info of the movie. it allows you to show you the movie file in your browser, play the movie in your default media player or in our customized media player, you can also delete the file associates to the movie         | GuiComponent   |
| QExplorer        | ExplorerWidget  | This component purpose is to add the folder you want the search movies files in and add it to the databases, in case a file can be parsed you can provide an IMDb url and it will get the info of the film                           | GuiComponent   | 
| QMovieListWidget | MovieListWidget | This widget displays the movies of a research                                                                                                                                                                                        | GuiComponent   |
| QMoviePlayer     | MoviePlayer     | This is the player media player.                                                                                                                                                                                                     | QDialog        |
| QError           | ErrorWidget     | Display error that we didn't catch                                                                                                                                                                                                   | QLabel         |
| QPoster          | QPoster         | This is a label that's enable to load movie poster asynchronously                                                                                                                                                                    | QWidget        |
| QStackedWidget   | ComponentArea   | This is frame is where all the frames are stored.                                                                                                                                                                                    | QStackedWidget |
| QSettings        | SettingsWidget  | This frame is used to change the settings.    
                                                                                                                                                                                       | GuiComponent   |
### MovieListWidget
#### Method updateWidgets(films)
argument films: a generator of objects model Movie
This method updates the list of films
ResultRow is the class which is an item in the MovieListWidget

### MovieWidget
`updateWidgets` updates widgets with the information of the given film in argument
argument film: a object model Movie

If the movie have one file 3 buttons are displayed: Play the movie, Show in explorer, Delete file from database and if the movie have more than one file a QListWidget appear with the different
files and the 3 three same buttons for each file. We use the class FileWidget (which is also in `QMovieWidget.py`)  as item of the QListWidget 

### SettingsWidget
The location where the settings are stored depend of your system:

Windows: `HKEY_CURRENT_USER\Software\CPNV\MAWIE`

MacOs: `$HOME/Library/Preferences/com.CPNV.MAWIE.plist`

Linux: `$HOME/.config/CPNV/MAWIE.conf`

#### Settings available
| Location             | Name            | Description                                                                                                                                                                    | Default value |
|----------------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| CPNV/MAWIE           | first launch    | this is used to know if it's the first time the program is lauchned                                                                                                            | true          |
| CPNV/MAWIE/infomovie | player-default  | this allows to only use the default media player when you're in the MovieInfo and you clicked on "play film"                                                                   | true          |
| CPNV/MAWIE/updator   | updator-enabled | this setting enable/disable the updator                                                                                                                                        | true          |
| CPNV/MAWIE/updator   | frequency       | if the updator is enabled this setting set the frequency the updator will execute its checking.there are predefined values : 300,1800,6000 and 3600 (they are in milliseconds) | 1800          |

### MovieListWidget
To update the list of films, use updateWidgets, it takes the fallowing argument:

argument data : it has to be a generator of model objects Movie


### MoviePlayer
The MoviePlayer use QMediaPlayer. the format/codec it allows you to read depends on your system:
 
on windows refer to DirectsShow 

on Mac refer to QuickTime Player

on Linux it depend on the installed Gstreamer plugins.
if you want to use the player you can just make an instance of it with the fallowing arguments:

argument path: the file path

and then execute it. It should looks like:

```
moviePlayer = MoviePlayer(path)
moviePlayer.exec_()

```

### ExplorerWidget
There is three other classes in the file `mawie.gui.component.QExplorer`: AddFilesWidget,FileParsedWidget and FileNotParsedWidget
AddFilesWidget holds the two lists : the list inherits from FileParsedWidget and the list inherits from FileNotParsedWidget.
FileParsedWidget and FileNotParsedWidget inherit from QListWidget and Listener. The first one is the list who displays the parsed file
and the second one the files which can't be parsed. the lists add the file as the explorer processed them

### ResearchWidget
#### Event used
| Event class    | Usage                                                                                                      |
|----------------|------------------------------------------------------------------------------------------------------------|
| SearchRequest  | is used to send a search                                                                                                        |
| SearchResponse | When handled, this event will call updateWidgets(event.data) with the response data (search results)       |

### ComponentArea
#### How to add a widget to the ComponentArea
create a file in ```mawie.gui.components``` (the location has no effect but it's just to keep the structure of the project).
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
Now you have to add it to the ComponentArea, In the file `QStackedWidget` in the method `initWidget` add this line:
`self.addWidget(MyWidget(self))`

### How to create a event
To create a event, go to the `mawie.event.gui` and a class which looks like
```Python
Class MyEvent(Event)
    pass
```

### How to switch the frames of the ComponentArea
To switch frames, you have to emit the Event `ShowFrame(TheNameOfYourWidget)`. it should looks like

```Python
self.gui.emit(ShowFrame(ShowFrame(FrameYouWantToShow.__name__)))

```

if you want to pass data with it, like a film for example, you can do it this way : 
`ShowFrame(FrameYouWantToShow.__name__, film)`