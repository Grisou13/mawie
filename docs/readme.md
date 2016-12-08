The different apis are documented here.

The app has multiple components:

The *database*, a simple SQlite database, which stores movie metadata.

The *gui*, which is the graphical implementation of the underlying apis (research, and gui)

The *research*, which handles searches for movies in the local movie database, and is able to query online services to retrieve movie metadata.

The *explorer*, which parses a directory on the hard drive and registeres found movies to the local movie database