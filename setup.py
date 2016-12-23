#!/usr/bin/env python
"""
Setup script used for setuptools.
"""
from distutils.core import setup
import sys
includes = [
    "sip",
    "PyQt5",
    "PyQt5.QtCore",
    "PyQt5.QtGui",
]
datafiles = [("platforms", ["C:\\Python34\\Lib\\site-packages\\PyQt5\\plugins\\platforms\\qwindows.dll"]),
            ('imageformats',['C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qjpeg4.dll',
                'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qgif4.dll',
                'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qico4.dll',
                'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qmng4.dll',
                'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qsvg4.dll',
                'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qtiff4.dll'
                ]),
             ("", [r"c:\windows\syswow64\MSVCP100.dll",r"c:\windows\syswow64\MSVCR100.dll"])]

requirements = []
with open("./requirements.txt","r+") as f:
    for l in f:
        requirements.append(l.strip())

setup(name='Mawie',
      version='0.0.1',
      description='Python gui allowing filtering of films on local harddrive',
      author='Thomas Ricci',
      author_email='thomas.ricci@cpnv.ch',
      url='https://github.com/Grisou13/mawie',
      include_package_data=True,
      zip_safe=False,
      platforms='any',
      requirements = requirements,
      packages=['mawie'],
      data_files=datafiles,
      entry_points = {
        'console_scripts': ['mawie.cli:start'],
        }
     )
