import argparse

parser = argparse.ArgumentParser(description='Mawie film indexer')

parser.add_argument("--search",dest="append")

def start():
    parser.parse_args()