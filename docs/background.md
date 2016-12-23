# What are background components?

These components are special, they do not interact directly with the Gui (like GuiComponents would); no, these communicate with what is called the ```App```.

They were implemented this way because of the way python works.
Long story short, in python there is the GIL (Global Interpreter Lock), which executes python threads.
The problem is that the gil executes them one after the other. Threads in python cannot be truly in parallel like in c++.
This has a nasty side effect, which is the Gui runs in a thread, and other processes that would take alot of CPU too.
The Gui runs Qt and Qt can only process itself if it has time to, but if another process takes all the CPU, the GIL won't allow the Gui thread to run (remember one after the other). It is convinient though, for memory and ressource locking and management.

Background process are therefor running in a separate thread which operates at a certain rate. Allowing the main thread to process while the background thread is in pause.

**They offer a non blocking way of getting data.**

# Creating a bg component

Creating a component is simple, it's the management that is hard.

First the compoenent must look like
```python
class TorrentSearcher(Listener):
    def handle(self,event):
        pass
```

Then you need to register it in the App, for that, add your compoenent in the ```App.background``` list

```python
...
class App(EventManager):
    ...
    background = [Explorer, googleIt, Research, *TorrentSearcher*]
```

# Handling events in a background process

Aboce we've discussed why background compoenents here are important. Now you need to work intelligently with them.
A ``` Tick ``` event is sent in every background process whenever the App is working. This allows you to either process objects every tick, or you could dispatch events, and work with them.
If you try and process a long list of items, maybe use events, and try to queue them.
Events that are emitted will be process every tick, not when emitted.

## Getting data back to the gui

If you need to get data back to the Gui, it's very simple.
Your new component should emit an event that is a ``` Response ```.
For example, after searching torrents, you would emit ``` TorrentSearchResponse(..list of torrents) ```. And automatically, this event will be sent back to the Gui, and emitted in every component.

**important** : when emitting responses, they will be dispatched in every GuiComponent.
