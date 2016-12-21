import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

if __name__ == '__main__':
    if len(sys.argv):
        from . import cli
        cli()
    else:
        from . import gui
        gui()
