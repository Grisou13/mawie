# Communication between gui Elements

# Communication between background Components

# Adding a background component

This is maybe the weirdest part of the app. To add a background service, you will need to create the class (seems legit) and make it extend ``` Eventable ```, and then register it in the App class.
After that you can pass data via events to the App, which will dispatch it to your component.

```python
from mawie.events import Eventable
class MyAwesomeDataFetcher(Eventable):
    pass
```


# Adding a gui component

Adding a component is really simple. You will need to create a class that extends the GuiComponent class

```python
from mawie.components import GuiComponent
class MyAwesomeComponent(GuiComponent):
    pass
```

This is litteraly it. This will register your component in the main window, and adds it to the event management loop. Now your class can receive events if you create the method ```handle(self,event) ```

The components use PyQt5 grid system, if you choose to use PySide or use a Qt design editor, this doc cannot help you... Please not that GuiComponent is internaly a QWidget.

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
*Reminder* all events are in the **app.events** module.
