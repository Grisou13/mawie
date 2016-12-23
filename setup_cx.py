"""
This file is used to create an executable. This doesn't work for now.
to build python setup_cx build_exe
to create an msi python setp_cx build_msi
More commands are available in the cx_freeze docs
"""
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
deps = [
    "re",
    "os",
    "sys"
]
incs = [
    "README.md","sqlite3.dll","conf/","resources/","scripts/",".cache/"
]
buildOptions = dict(packages = deps, excludes = [],includes = deps,include_files = incs)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('mawie/__main__.py', base=base, targetName = 'mawie.exe')
]

setup(name='Mawie',
      version = '0.0.1',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables
      )
