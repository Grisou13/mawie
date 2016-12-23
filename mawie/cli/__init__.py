import argparse
import sys
from mawie import gui
parser = argparse.ArgumentParser(description='Mawie film indexer. \n This cli is not fully implemented yet.')

parser.add_argument("--inspire",action='store_true', required = False)
parser.add_argument("--gui",action='store_true', required = False)
parser.add_argument("--resources",action='store_true' ,required = False)
import mawie.helpers as h
from subprocess import call
import os
def createResources():
    print("fetching resources in : " + h.BASE_PATH+"/resources/")
    for d,dn,fn in os.walk(h.BASE_PATH+"/resources/"):
        for f in fn:
            if f.endswith(".qrc"):
                cmd = "pyrcc5.exe  -o "+os.path.join(h.BASE_PATH,"mawie/gui/resources/",os.path.splitext(os.path.basename(f))[0])+ ".py " +os.path.join(h.BASE_PATH,"resources/",f)
                call(cmd)


def start():
    args = parser.parse_args()
    if len(sys.argv) < 2:
        gui()
    elif args.inspire:
        print("SOME SUPER MAGIC QUOTE")
    elif args.gui:
        gui()
    elif args.resources:
        print("creating resources...")
        createResources()
        print("done!")
