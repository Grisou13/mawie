---
title: Mawie
revealOptions:
    transition: 'fade'
---
# Mawie
> Par Ilias, Thomas et Eric

# Tbl des matières
- Technologies
- BDD & Modèles
- Composants
  - Gui
  - Explorer
  - Search
  - Updator
  - Event handling
- Bugs restants
- Améliorations
- Conclusion
- Q/A

# Technologies
 - Python3
 - SqlAclhemy (ActiveAlchemy)
 - sqlite3
 - PyQt5
 - Tkinter (déprecié)

 On a développé l'application pour qu'elle soit orienté événement (comme une application Android).

# BDD & Modèles

 <img src="./img/mld.png"/>

 Note: données du dump de la librairie imdbpie

 
# Composants

<img src="./img/composants.png"/>

# Search
Recherche sur les 2 modèles, ou autre.

- Namepsace : mawie.research

- Recherche Simple
- Recherche Avancé sur les modèles par defaults
- Recherche Avancé

##^ Recherche simple
```python
  from mawie.research.research import Research
  from mawie.models.movie import Movie
  searchable = Research()
  res = searchable.query("Some awesome movie title")
  for elem in res:
    assert isinstance(elem, Movie)
    print(elem.title)
```

##^ Recherche Avancé
```python
... imports
searchable = Research()
res = searchable.query("Some awesome movie title",["desc","actors"])
for elem in res:
    assert isinstance(elem, Movie)
    print(elem.title)
```

##^ Recherche Avancé (2)

```python
... imports
searchable = Research()
res = searchable.query({Movie:{"release":{"gte":"2010-01-01","lte":"2016-01-01"}}})
for elem in res:
    assert isinstance(elem, Movie)
    print(elem.title)
```

# Explorer

- Qu'est-ce que c'est
- Namespace : mawie.explorer
- Utilise des Apis (duckduckgo, et imdb)

##^ 1ère approche : Comparateur de chaine de caractère

_"La distance de Levenshtein est une distance mathématique donnant une mesure de la similarité entre deux chaînes de caractères. "_
Lowercase/Uppercase
```python
    >>> from Levenshtein import distance
    >>> distance("La vie d'adèle", "La.vie.d'adele.french")
    >>> #           ^   ^    ^  ^
    10
```
Taux minimum pour validation : ~80%.

Note:

La distance levenstein est égale au nombre minimal de caractères qu'il faut supprimer, insérer ou remplacer pour passer d’une chaîne à l’autre.

##^ 2ème approche : Utilisation de duckduckgo

Dans un dexuipme temps on a développé une solution plus simple. On recherche le nom du film donnée par Guessit sur duckduckgo.
Cela permet de le traduire, et d'avoir beaucoup plus souvent des résultat de recherche cohérent (dépendant du film).
Après avoir récupéré le contenu imdb, on fait un test de semblance entre le nom Guessit, et le nom retiré IMDB pour vérifier que l'on ait bien trouvé le bon film, puis on l'inspre dans la base de donnée.

# Updator

Execute une tache périodiquement.



# Gui

## Les différentes fenêtres

<img src="./img/guiSchema.png" /></div>

##^ ajouter un dossier

<img src="./img/addFolder.png"/>

##^ Affichage le contenu d'une recherche

<img src="./img/list.png"/>

##^ Affichage des informations d'un film

<img src="./img/film.png"/>

##^ Lire le film

<img src="./img/player.png"/>

##^ Recherche avancée

<img src="./img/asearch.png"/>

##^ Settings

<img src="./img/settings.png"/>

# Gestion d'événement

<img src="img/pexels-photo-186537.jpeg" />

Note:

Tous les composants de l'application communique selon

##^ Entre composants QT

On utilise les singaux Qt, et ensuite on communique les données à l'arrière plan avec le système d'événement.

##^ Entre service d'arrière plan

On utilise une solution faite maison qui reprend l'idée d'un MessageBroker (AMQT, ZeroMq, etc...)


<img src="./img/event-loop-2.png"/>

Note:

On fait tourner un event loop dans le GUI (pour passer les données à l'arrière plan).

On fait tourner un Event loop dans un thread à part pour processer les événements toute les .25s (pour le pas surgargé le thread principale QT!)

Tout ça a cause du GIL

# Améliorations

- Gui
- Explorer
- Recherche
- Updator
- Système d'événements
- Implémenter complétement le cli

##^ Gui

- Améliorer l’ergonomie

- Rendre plus responsive

- Faire une fenêtre adaptée pour les séries

- Ajouter la possibilité de donner un nom de film
pour les fichiers qui n’ont pas été parsés

- Indiquer le film comme «viewed» lorsqu’on a -cliquer sur le bouton «play film»

##^ Explorer

- Permettre d'utiliser le module synchronement
```python
... imports
e = Explorer()
e.parseDirectory("path/to/my/super/movie/dir")
```
- Gérer la perte de connexion à internet
- Gérer des sources différentes pour la recherche d'information
- Inclure l'utilisateur lors du parsing dans le cas ou un fichier n'est pas trouver

##^ Recherche

- Mettre en cache les requetes

##^ Updator

- Ajouter d'autre taches à faire
- Permettre à des class d'enregistrer de nouvelle tache a faire
- Permettre à l'utilisateur de séléctionner les taches à exéctuer

##^ Système d'événements

- Ajouter une Queue pour les message en retour

- Permettre de dispatcher un événement à un object particulier

Note:

Utiliser une queue de message de retour pour ne pas occuper la queue d'événement principale

# Bugs restants

- Gui
- Explorer
- Research
- Système d'événement

##^ Gui
- La fenêtre dépasse si l’écran est trop petit
- Pas de gestion des formats non pris en charge par le lecteur media personnalisé
- Sous Linux, le fichier ne se montre pas dans l’explorer

# Conclusion

# Question
```python
import sys
sys.stdout.write("Questions ? ")
```
