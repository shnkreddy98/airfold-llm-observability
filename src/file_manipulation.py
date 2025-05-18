import os
import json

datadir = './data'

def initialize(filename, statesave):
    filename = os.path.join(datadir, filename)
    statesave = os.path.join(datadir, statesave)

    if not os.path.exists(datadir):
        os.makedirs(datadir)

    if not os.path.exists(statesave):
        with open(statesave, 'w+') as f:
            f.write(str(0))

def read_file(filename, filetype='txt'):
    filename = os.path.join(datadir, filename)
    if filetype=='txt':
        with open(filename, 'r') as f:
            return int(f.read())
    else:
        with open(filename, 'r') as f:
            return json.load(f)

def write_file(filename, val, filetype='txt'):
    filename = os.path.join(datadir, filename)
    if filetype=='str':
        with open(filename, 'w+') as f:
            f.write(str(val))
    else:
        with open(filename, "w+") as f:
            json.dump(val, f, indent=2)

