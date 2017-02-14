# Mawie

#### Par Ilias, Thomas et Eric

---
# Tbl des matières
- Technologies
- Explorer
- Search
- BDD & Modèles
- Gui
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
 
---

# Search

Recherche sur les 2 modèles, ou autre.

Possibilité de séléctrionné n'iimporte quelle donnée en utilisant une syntax particulière

```python
from mawie.research.research import Research
from mawie.models.movie import Movie
searchable = Research()
res = searchable.query("Some awesome movie title")
for elem in res:
  assert isinstance(elem, Movie)
  print(elem.title)
```


```python
... imports
searchable = Research()
res = searchable.query("Some awesome movie title",["desc","actors"])
for elem in res:
  assert isinstance(elem, Movie)
  print(elem.title)
```

```python
... imports
searchable = Research()
res = searchable.query({Movie:{"release":{"gte":"2010-01-01","lte":"2016-01-01"}}})
for elem in res:
  assert isinstance(elem, Movie)
  print(elem.title)
```


---
# BDD & Modèles

<div style="text-align:center">
<img src="./img/mld.png"  height="550px"/></div>

---

# Gui : navigation
## Les différentes fenetres

---

# Gui : Fenêtres
## ajouter un dossier
<div style="text-align:center">
<img src="./img/addFolder.png"  height="550px"/></div>

---

# Gui : Fenêtres
## Affichage le contenu d'une recherche
<div style="text-align:center">
<img src="./img/list.png"  height="550px"/></div>

---

# Gui : Fenêtres
## Affichage des informations d'un film
<div style="text-align:center">
<img src="./img/film.png"  height="550px"/></div>

---

# Gui : Fenêtres
## Lire le film
<div style="text-align:center">
<img src="./img/player.png"  height="550px"/></div>

---

# Gui : Fenêtres
## Recherche avancée
<div style="text-align:center">
<img src="./img/asearch.png"  height="550px"/></div>

---

# Gui : Fenêtres
## Settings
<div style="text-align:center">
<img src="./img/settings.png"  height="550px"/></div>

---

# Gui : Améliorations
- Améliorer l’ergonomie

- Rendre plus responsive

- Faire une fenêtre adaptée pour les séries

- Ajouter la possibilité de donner un nom de film
pour les fichiers qui n’ont pas été parsés

- Indiquer le film comme «viewed» lorsqu’on a -cliquer sur le bouton «play film»

---

# Gui : Bugs restants

- La fenêtre dépasse si l’écran est trop petit
- Pas de gestion des formats non pris en charge par le lecteur media personnalisé
- Sous Linux, le fichier ne se montre pas dans l’explorer

---

# Communication entre composants
