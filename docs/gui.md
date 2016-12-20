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
| QSettings        | SettingsWidget  | This frame is used to change the settings.                                                                                                                                                                                           | GuiComponent   |
                                                                                                                                                                                                                    
### MovieListWidget
#### Method updateWidgets(films)
| method name   | param                           | description                                                  |
|---------------|---------------------------------|--------------------------------------------------------------|
| updateWidgets | films:generator of movie model  | updates the list of films with the filmes in the param films |
ResultRow is the class which is an item in the MovieListWidget

### MovieWidget
| method name   | param       | description                                                        |
|---------------|-------------|--------------------------------------------------------------------|
| updateWidgets | movie model | updates widgets with the information of the given film in argument |


If the movie have one file 3 buttons are displayed: Play the movie, Show in explorer, Delete file from database and if the movie have more than one file a QListWidget appear with the different
files and the 3 three same buttons for each file. We use the class FileWidget (which is also in `QMovieWidget.py`)  as item of the QListWidget 

### SettingsWidget
The location where the settings are stored depends on your system, please refer to the [QT docs](http://doc.qt.io/qt-5/qsettings.html#platform-specific-notes)



#### Settings available
| Location             | Name            | Description                                                                                                                                                                    | Default value |
|----------------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| CPNV/MAWIE           | first-launch    | this is used to know if it's the first time the program is lauchned                                                                                                            | true          |
| CPNV/MAWIE/infomovie | player-default  | this allows to only use the default media player when you're in the MovieInfo and you clicked on "play film"                                                                   | true          |
| CPNV/MAWIE/updator   | updator-enabled | this setting enable/disable the updator                                                                                                                                        | true          |
| CPNV/MAWIE/updator   | frequency       | if the updator is enabled this setting set the frequency the updator will execute its checking.there are predefined values : 300,1800,6000 and 3600 (they are in milliseconds) | 1800          |


### MoviePlayer
The MoviePlayer use QMediaPlayer. the format/codec it allows you to read depends on your system:
 
on windows refer to DirectsShow 

on Mac refer to QuickTime Player

on Linux it depend on the installed Gstreamer plugins.
if you want to use the player you can just make an instance of it with the fallowing arguments:

To display the widget MoviePlayer you have to instance it. it take only one parameter: path - it simply the path to the file to read

and then execute it. It should looks like:

```
moviePlayer = MoviePlayer(path)
moviePlayer.exec_()

```

### ExplorerWidget
TODO REXPLIQUER CETTE MERDE
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

class MyWidget(GuiComponent):
    def __init__(self,parent = None):
        super().__init__(parent)
```
This is literally it. This will register your component in the main window, and adds it to the event management loop. Now your class can receive events if you create the method handle(self,event)

The components use PyQt5 grid system, if you choose to use PySide or use a Qt design editor, this doc cannot help you... Please note that GuiComponent is internally a QWidget.

We recommend setting up a ```initWidget(self)``` or ```initUi(self)``` method on your class

```python
from mawie.components import GuiComponent
class MyAwesomeComponent(GuiComponent):
    def __init__(self,parent = None):
        super(MyAwesomeComponent,self).__init__(parent)
        #instantiate some helpers and create some data if needed
        self._data  = {} # data :D
        self.initWidget()
        self.show()#don't forget to call show, otherwise the component may not appear
    def initWidget(self):
        layout = QGridLayout(self)
        self.setLayout(layout)
     
```

Now if you need to pass data to the background, or need to receive some data, you will need to overide the ``` handle(self,event) ``` method.
If you override ``` handle ``` please call ```super().handle(event)```

```python
from mawie.components import GuiComponent
from mawie.events import Start
from PyQt5.QtWidgets import QGridLayout

class MyAwesomeComponent(GuiComponent):
    def __init__(self,parent = None):
        super(MyAwesomeComponent,self).__init__(parent)
        #instantiate some helpers and create some data if needed
        self._data  = {} # data :D
        self.initWidget()
        self.show()#don't forget to call show, otherwise the component may not appear
    def initWidget(self):
        layout = QGridLayout(self)
        self.setLayout(layout)
    def handle(self,event):
        super(MyAwesomeComponent,self).handle(event)
        if isinstance(event,Start):
            pass # do something on start of the app
```


Now you have to add it to the ComponentArea, In the file `QStackedWidget` in the method `initWidget` add this line:
`self.addWidget(MyWidget(self))`

#### How to display your frame store in ComponentArea
To switch frames, you have to emit the Event `ShowFrame(MyNewWidget.__name__)`. it should looks like
```Python
    from mawie.events.gui import  ShowFrame
    
    def displayMyWidget(self):
        self.gui.emit(ShowFrame(MyWidget.__name__))

```
if you want to pass data with it, like a film for example, you can do it this way : 
`ShowFrame(WidgetYouWantTODisplay.__name__, film)`

## How to create a event
To create a event, please refer to event doc (docs.event.md)


