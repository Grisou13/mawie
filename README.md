Mawie
===========

# What is this all about

Mawie is a project with educative purpose. The concept is simple : the application manage for you your movies files. It parses it, get the information about your movies, and display it to you with little extras.


Python is one of technologies that you hear myths about, and always want to test. This is the perfect way to test alot of functionnality from it. From database queries, to handling files, and having a gui application behind.

Python was used, because we knew it would fit our needs and even more. We were able to achieve a good balance between readable code, and efficient code, and all that thanks to python builtins, and simple module system.

Documentation is available in the [docs](docs/) folder

# Installation Guide

Requirements :
- [Python](https://www.python.org/downloads/release/python-352/) 3.5.2
- [pip](https://packaging.python.org/installing/#install-pip-setuptools-and-wheel) 9.0.1 or greater

First, install the sources of the project
```
git clone https://github.com/Grisou13/mawie.git && cd mawie
```

In the cloned folder, install the requirements with pip.
(if you have many versions of python installed, use "pyton3.5 -m pip" to assure that you use pip that correspont to the good version).
```
python3.5 -m pip install -r requirements.txt
```

And to start the app simply
```
python3.5 mawie
```

# Bugs issues

There are no real bugs to signal as of this release.
If something happens, please be sure to dive into the logs, or atleast include them.

If you find something, please either submit an [issue](https://github.com/Grisou13/mawie/issues/new),
or a create fork and submit a pull request.

# Tests performed

No unit tests where made.

# Todos

We could do alot more. Here's a list of improvements that need to be done:

- Allow a non parsed file to be manually given a url, or title.
- Refactor the explorer and googleit to work as standalone components.
- Write some tests !!
- Make a welcome page on first launch (A settings is already registered for that).
- make a setup.py with cx_freeze that makes an executable out of mawie.
- Improve event system, or pass directly on asyncio

# License

Copyright [2016] [Ilias - Thomas - Eric]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.



Refactor and add relative imports, sintead of this horrible sys.path.extend
UZse asyncrounous coroutines to boost app performance (Quamash, Eventloops, or pure python async)

http://docs.themoviedb.apiary.io/#reference/search/searchmovie/get
theme : https://github.com/ColinDuquesnoy/QDarkStyleSheet
