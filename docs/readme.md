The different apis are documented here.

The app has multiple components. Every component can be used as a standalone, in any futur developpement.

The *database*, a simple SQlite database, which stores movie metadata. Models where created to handle queries (this app was not made in 1970).

The *research*, which handles searches for movies in the local movie database, and is able to query online services to retrieve movie metadata.

The *explorer*, which parses a directory on the hard drive and registeres found movies to the local movie database

The *gui* is made in Qt (PyQt5). It uses the updator, and everything else to make it run.

It was made easy for anybody with some minimum of python, and qt notions to add components to the Gui, or add functionality to underlying apis.

# folder structure

libs/ contains python librairies that were either altered in functionalilty, or were installation failed, so we installed them from source.

# Todos

* relative imports (pycharm adds the root of the project to sys.path, which makes imports a bit faster, but not cleaner)
* research search online apis
* make cli for the app
* make torrent download for gui, and api