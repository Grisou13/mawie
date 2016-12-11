# Communication between gui Elements

# Communication between background Components

# Adding a component

Adding a component is really simple. You will need to create a class that is a QWidget, and extends the GuiComponent class

```python
class MyAwesomeComponent(QWidget,GuiComponent):
    pass
```

This is the basics. This will register your component in the main window, and adds it to the event management loop. Now your class can receive events if you create the method ```handle(self,event) ```
*Reminder* all events are in the **app.events.gui** module.