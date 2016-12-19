# Using the search

It's the most easy thing. just create a ```Research``` object, and call the ```query``` method.

```python
from mawie.research.research import Research
from mawie.models.movie import Movie
searchable = Research()
res = searchable.query("Some awesome movie title")
for elem in res:
  assert isinstance(elem, Movie)
  print(elem.title)

```
The ```query``` returns a generator, that you can iterate on easily. It returns instances of movies.

## Advanced querying

If you want to make more complex queries than just searching for movie titles; you can use the ```filter``` in the query method. This will execute your query on every field put in the filter.
```python
from mawie.research.research import Research
from mawie.models.movie import Movie
searchable = Research()
res = searchable.query("Some awesome movie title",["desc","actors"])
for elem in res:
  assert isinstance(elem, Movie)
  print(elem.title)
```
This query will search for "Some awesome movie title" in the title, desc, and actors field of the Movie model.

### Super advanced querying

Now if you really, really need to get something specific from the database, you can pass a dict to the query.
The dict looks like this ```{ModelClassReference: {ComplexQueryData}}```. THe query structure is really simple, it's based out of ElasticSearch query syntax (implemented by the awesome module [sqlalchemy_elasticquery](https://github.com/loverajoel/sqlalchemy-elasticquery) ). Please go check out the docs for it.

Now what this allows is queries with date ranges
```python
from mawie.research.research import Research
from mawie.models.movie import Movie
searchable = Research()
res = searchable.query({Movie:{"release":{"gte":"2010-01-01","lte":"2016-01-01"}}})
for elem in res:
  assert isinstance(elem, Movie)
  print(elem.title)
```
This query will retrieves every movie between 2010-2016.

## Swithing models

If you decide you had enough and just want to query another model, you create your search object by passing a reference to the model.

```python
from mawie.models.file import File
searchable = Research(model=File)
```

Or by calling the method ```setModel(ModelClass)```

```python
from mawie.models.file import File
searchable = Research()
searchable.setModel(File)
```

Now what this doesn is by useing a normal query with only string params, you can now change the model on which it wil be queried. This is usefull if you want to use the search for querying multiple models, without having to pass by the standard sqlalchemy objects. These methods where built for conviniency.

## Adding, or setting custom columns to query

It's the same process as in Switching models. Except the props are ```Research(cols = [ListofColumnsToQuery])```,
or ```setColumns([ListofColumnsToQuery])```.

# Events for search

| Event class    | props                 | data type        | usage                                                               |
|----------------|-----------------------|------------------|---------------------------------------------------------------------|
| SearchRequest  | data                  | str,dict         | Send a request to the search api, and it will emit a SearchResponse |
| SearchResponse | request, responseData | Event, generator | Request response                                                    |

# Where it searches

As of right now, release 0.0.1-rc1, the research will only make queries to the local database.
However, making it possible to query secondary apis would be possible and potenitially, staright forward, since the GoogleIt class exists.

# Search classes and api
