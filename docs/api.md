# Component constructors in app/gui/components

Movie ( RootTkinter, MovieModel )
MovieList (RootTkinter, [MovieModel] )

DirectoryListing ( RootTkinter, [File] )
ResearchResultList ( RootTkinter, [SearchableItems] )

ResearchResultItem ( RootTkinter, SearchableItem)


# Components

Models/Settings
    getSearchableFolders()

Models/File

Models/Movie

research/SearchableItem
    getData()


research/search
    searchMovie()
    searchPerson()
    search(term, itemType)

App
    boot()
    getUserSettings()
    getConfig()


# Constants

BASE_PATH = root to folder mowie
CACHE_PATH = BASE_PATH/.cache


sdf