# Why events and not just python async?

I can understand the question, and the answer is very simple. Qt doesn't play well with async.
The other problem is, how would it be possible to add data passing through compoenents at runtime with signals, well that's ok for Gui compoenents, what about background processes then, bound them to Qt so if we want to create a web service or a cli we need to recreate them?

We decided to create a very simple event system. It allows us to pass data back and forth in the app and all it's components. Simple?

Events are small objects that allow data to transit between elements in our App.
They are in some way asyncrounous, which means that when an action is done somewhere that emits an event, something else can response to it in a non blocking way.


The event system was created because of the limitation of the python language. The GIL (Global Interpreter Lock) in python is the reason why. You can [read more here](http://www.dabeaz.com/python/UnderstandingGIL.pdf) if you want more details.

There are 3 main classes to understand for all this event mayhem :

 - *EventManager*. The main class, the man, this class handles event from components and is used to coordonate them.
 - *listener* This is a class that will listen for events. This class is registered in an event manager which dispatches event to it
 - *Event*. The actual event objewct which is passed in the event manager, and dispatched to listeners.

Most of the components in the app use events. And some GuiComponents use Qt signals, and events.

# Event dispatching and how to do it

The most basic example of events, and how they work is in the mawie.app. The class App is an EventManager. And for the example, the Search is a listener.
The Search will listen for events of the App, and when a SearchRequest is thrown in the App, the search will respond to it, and actually do a query in the database.
This allows for asynchrounous computation. It does however complicate the process of managing your events.

The search example is really simple. But what if we needed to do aaaallooooot of work. Well you would first off need to break it down into managable peaces. Take the mawie.explorer.Explorer as an example.
The explorer needs to parse a directory and return movie info based on the filename. Doesn't seem complicated ? ... Well you actually need to do alot of queries for that to work.
Since queries take time, you can't just all run them at once.... that would not be ideal. You need to create events, and when, for example a query response is emitted, continue parsing.

# Handling events

Handling events isn't black magic, nor is it a black box. Make sure that the component (GuiComponent, or BackgroundProcess) is registered in an event manager (Gui, or App).
Then your component must implement the ```handle(self,event)``` method. This method is called whenever an event was triggererd in the event manager.
That's it. now in your handle method you could check for the type of event with ```isinstance(event,EventType)``` (remember events are classes?).
Or you could verify it's data that are in ```event.data```.

# Creating an event manager

Now the real work. well, not that much. Creating an event manager is really simple. You just need to have listeners and register them before starting any event loop.
What you would idealy want is on instanciation of your manager, register the listeners.

```
from mawie.events import EventManager,Listener

class MyAwesomeListener:
    pass

class MyNewEventManager(EventManager):
    def __init__(self):
        myAwesomeListener = MyAwesomeListener()
        self.registerListener(myAwesomeListener)
```

Now that will make the listener be able to listen for events, but not really send back any, not really usefull.
To add emitting you could do 2 things :
- Pass the event manager in the __init__ of your listener, and then save the eventManager in your class and do something like ```self.eventManager.emit(SomethingHappened())```
- Or assign the emit method to the event manager's emit function (It's a small hack in a way, but works really well)

This would give you :

```python
from mawie.events import EventManager, Listener

class MyAwesomeListener:
   def __init__(self,eventManager):
        self.manager = eventManager
   def dummy(self):
        self.manager.emit(SomeDummyEvent())

class MyNewEventManager(EventManager):
    def __init__(self):
        myAwesomeListener = MyAwesomeListener(self)
        myAwesomeListener.emit = self.emit
        self.registerListener(myAwesomeListener)
```

OR

```python
from mawie.events import EventManager

class MyAwesomeListener:
    pass
class MyNewEventManager(EventManager):
    def __init__(self):
        myAwesomeListener = MyAwesomeListener()
        myAwesomeListener.emit = self.emit
        self.registerListener(myAwesomeListener)
```

I find the second method to be more practical, but it feels really hacky. It's up to you now to decide with what you are more comfortable with.

# Creating an event loop

This is a very trivial process. You can take example on the class mawie.app.App. You emit a ```Start``` event to the manager, and then what that does is just create a while true loop.
```python
from mawie.events import Start,Tick
import time

....Super class def ...
def handle(self,event):
    if isinstance(event,Start):
        while True:
            self.emit(Tick())
            time.sleep(.5)
    if isinstance(event,Tick):
        pass # Do some work :D
```


Events are objects allowing compoenents (any compoenent) to talk to each other.

Events have timeouts, by default they don't (event.timeout == 1), this means that it will be able to cycle only once in the app before getting destroyed.

# How events work with the gui

Events are passed between Gui events if they need to change frames.

We created 2 special event classes
- *Request*
- *Response*

These 2 classes are dispatched between the background process and the gui. So to get data from Gui to the background you would emit a sublass, or a Request. And then in a background process you would emit a Reponse (or sublclass).

# List of events

Everything below will be listed from the namespace mawie.events

| Event class | props                         | data type          | usage                                          |
|-------------|-------------------------------|--------------------|------------------------------------------------|
| Event       | data                          | any                | Main event class.                              |
| Request     | data                          | any                | Event forwarded to background process          |
| Response    | request , data                | Request, any       | Event that is forwarded from background to gui |
