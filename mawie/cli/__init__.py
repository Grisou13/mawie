import argparse
import sys
from mawie import gui
parser = argparse.ArgumentParser(description='Mawie film indexer. \n This cli is not fully implemented yet.')

parser.add_argument("--inspire",action='store_true', required = False)
parser.add_argument("--gui",action='store_true', required = False)
def start():

    args = parser.parse_args()
    if len(sys.argv) < 2:
        gui()
    elif args.inspire:
        print("SOME SUPER MAGIC QUOTE")
    elif args.gui:
        gui()
