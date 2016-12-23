Mawie has multiple components. All components were ment to be used as standalones, and in a whole app.

The *database*, a simple SQlite database, which stores movie metadata. Models where created to handle queries (this app was not made in 1970).

The *research*, which handles searches for movies in the local movie database, and is able to query online services to retrieve movie metadata.

The *explorer*, which parses a directory on the hard drive and registeres found movies to the local movie database

The *gui* is made in Qt (PyQt5). It uses the updator, and everything else to make it run.

It was made easy for anybody with some minimum of python, and qt notions to add components to the Gui, or add functionality to underlying apis.

The app runs under a global event system. It is used to pass data back and forth in the app. Events are used for the communication between components.
The event system is really basic. It allows to emit events, and listen to them.

# Todos

* relative imports (pycharm adds the root of the project to sys.path, which makes imports a bit faster, but not cleaner)
* research search online apis
* make cli for the app
* make torrent download for gui, and api


#Put this in?
tl;dr The GIL blocks thread execution. This may be convenient, but in our case, we need Qt to run, and make background process data happen. If we were to only use 2 threads, and no event system, Qt will crash if too much data needs to be processed in the backend. This also has another negative side effect : alél the bandwidth is used for making single requests to duckduck go or imdb.... sems a bit too much?
