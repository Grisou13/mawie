import sys
import os

sys.path.append(os.path.join(__file__, "../../"))
sys.path.append(os.path.join(__file__, "../"))
print("yo")
if __name__ == '__main__':
    from .__main__ import run
    run()