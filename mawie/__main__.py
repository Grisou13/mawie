import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
def run():
    from mawie.gui.Qgui import start
    app = start()
if __name__ == '__main__':
    run()
