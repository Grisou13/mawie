import sys
import os

sys.path.append(os.path.join(__file__, "../../"))
sys.path.append(os.path.join(__file__, "../"))
print("asdasdasdasd")
def run():
    from mawie.gui.Qgui import Gui
    app = Gui.start()
if __name__ == '__main__':
    run()