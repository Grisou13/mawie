import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
if __name__ == '__main__':
    from .__main__ import run
    run()
