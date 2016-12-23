import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

if __name__ == '__main__':
    from mawie import cli
    cli()
