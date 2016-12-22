# GUI
At the beginning of the project, we chose to use Tkinter but we find a little bit incomplete for what we would  like to do
so, we decide to change to pyqt.

## Little manual for GUI application use
__add a folder__:
* in the menu bar go to add folder 
* select a folder

__delete a folder__:
* in the menu bar go to settings
* in the list, delete the folder you want to delete. it will delete all the files and the associated movies from the database

__change settings__:
Go to settings in the menu bar, change the settings and change the settings you want to change. The settings are automatically saved on change

__make advanced research__:
* in the menu bar, go to research-> advanced search
* complete the form (you don't have to fill all the input)
* click on the button search at the bottom


__delete a movie/file__:
if you want to delete a movie or a file from the database:
* search the movie in the movie list
* click on see info
* at the bottom of the window, there is a button delete movie from database
* if there is more than one file associates to the movie, there is a list with all the files
    * found the file you want to delete and click on delete the file from database 




### MainWindow
This is the widget which hold the ResearchWidget and the ComponentArea.

## Listing of graphical component
We chose to put a "Q" in the front of the filename of every graphical component. These components are all in the
directory ``` mawie.gui.components ```


| Filename         | Class name      | Description                                                                                                                                                                                                                          | Inherited from |
|------------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| QResearchWidget  | ResearchWidget  | This component communicates with ```mawie.research.search```,to launch research and then emit an event to QMovieListWidget to show results                                                                                           | GuiComponent   | 
| QAdvancedSearch  | AdvancedSearch  | display the form to do advanced research                                                                                                                                                                                             | GuiComponent   |
| QMovieWidget     | MovieWidget     | Display the info of the movie. it allows you to show you the movie file in your browser, play the movie in your default media player or in our customized media player, you can also delete the file associates to the movie         | GuiComponent   |
| QExplorer        | ExplorerWidget  | This component purpose is to add the folder you want the search movies files in and add it to the databases, in case a file can be parsed you can provide an IMDb url and it will get the info of the film                           | GuiComponent   | 
| QMovieListWidget | MovieListWidget | This widget displays the movies of a research                                                                                                                                                                                        | GuiComponent   |
| QMoviePlayer     | MoviePlayer     | This is the player media player.                                                                                                                                                                                                     | QDialog        |
| QError           | ErrorWidget     | Display error that we didn't catch                                                                                                                                                                                                   | QLabel         |
| QPoster          | QPoster         | This is a label that's enable to load movie poster asynchronously                                                                                                                                                                    | QWidget        |
| QStackedWidget   | ComponentArea   | This is frame is where all the frames are stored.                                                                                                                                                                                    | QStackedWidget |
| QSettings        | SettingsWidget  | This frame is used to change the settings.                                                                                                                                                                                           | GuiComponent   |

### QPoster
This widget takes two arguments: 

parent: QWidget (Default value None)

url : str (Default value None)

#### Method                                                                                                                                                                                                         
| Method name   |  Parameters                     | description                                                                                                                    |
|---------------|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| updateUrl     | url: str                        | update the image with the image of the given url. if the image can't be loaded or if there is no image it take a default image |

### MovieListWidget
#### Method
| Method name   |  Parameters                     | description                                                  |
|---------------|---------------------------------|--------------------------------------------------------------|
| updateWidgets | films:generator of movie model  | updates the list of films with the filmes in the param films |

ResultRow is the class which is an item in the MovieListWidget

### MovieWidget
| Method name   | Parameters       | description                                                        |
|---------------|------------------|--------------------------------------------------------------------|
| updateWidgets | data:movie model | updates widgets with the information of the given film in argument |



If the movie have one file 3 buttons are displayed: Play the movie, Show in explorer, Delete file from database and if the movie have more than one file a QListWidget appear with the different
files and the 3 three same buttons for each file. We use the class FileWidget (which is also in `QMovieWidget.py`)  as item of the QListWidget 

### SettingsWidget
The location where the settings are stored depends on your system, please refer to the [QT docs](http://doc.qt.io/qt-5/qsettings.html#platform-specific-notes)

To instance a QSettings you have to give the name of company and the name of your soft as parameter or set them in the QApplication, we choose the last solution:

The name of the application is `MAWIE`

The name of the organization is `CPNV`

if you want to changed them go to `mawie.gui.QGui.py` in the function `start()` and change the two line:

```python
    app.setOrganizationName("CPNV")
    app.setApplicationName("MAWIE")
```

#### Settings available
| Key name                | Description                                                                                                                                                                    | Default value |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| first-launch            | this is used to know if it's the first time the program is lauchned                                                                                                            | true          |
| player-default          | this allows to only use the default media player when you're in the MovieInfo and you clicked on "play film"                                                                   | true          |
| updator/updator-enabled | this setting enable/disable the updator                                                                                                                                        | true          |
| updator/frequency       | if the updator is enabled this setting set the frequency the updator will execute its checking.there are predefined values : 300,1800,6000 and 3600 (they are in milliseconds) | 1800          |


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

This class holds the class `AddFilesWidget`.
In `AddFilesWidget`, there are two more classes `FileParsedWidget` which displays the parsed file and `FileNotParsedWidget` which displays
the not parsed file.


#### AddFilesWidget
##### Methods
| Method Name      | Parameter                               | Description                                                                                    |
|------------------|-----------------------------------------|------------------------------------------------------------------------------------------------|
| scanDir          | None                                    | Emit the event ParseDirectoryRequest with the selected dirdirectory path in chooseDir          |
| chooseDir        | None                                    | Display a QFileDialog to choose a directory, when we chose a directory call the method scanDir |
| getFilmInfoByUrl | item : QListWidgetItem \|\|  file : str | ask for the IMDb url of the movie then add it to the db                                        |

##### Event used
| Event class           | Usage                                                            |
|-----------------------|------------------------------------------------------------------|
| ParseDirectoryRequest | this event is emit to ask the explorer to ParseDirectoryRequest  |




#### FileParsedWidget
###### Event used 



#### FileNotParsedWidget
##### Methods
###### Event used


### ResearchWidget
#### Event used
| Event class    | Usage                                                                                                      |
|----------------|------------------------------------------------------------------------------------------------------------|
| SearchRequest  | is used to send a search                                                                                   |
| SearchResponse | When handled, this event will call updateWidgets(event.data) with the response data (search results)       |



#### How to create a Gui component
create a file in ```mawie.gui.components``` (the location has no effect but it's just to keep the structure of the project).
You have to inherits the class of your graphical component from GuiComponent which allows to receive event. 

```Python
from mawie.gui.components import GuiComponent

class MyWidget(GuiComponent):
    def __init__(self,parent = None):
        super().__init__(parent)
```
This will register your component in the main window, and adds it to the event management loop. Now your class can receive events if you create the method handle(self,event)

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
### ComponentArea
#### How to add a widget to the ComponentArea
First you have to create a Gui Component then, you have to add it to the ComponentArea, In the file `QStackedWidget` in the method `initWidget` add this line:
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

