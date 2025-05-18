import os
import json
import yaml

datadir = './data'

def initialize(filename, statesave):
    filename = os.path.join(datadir, filename)
    statesave = os.path.join(datadir, statesave)

    if not os.path.exists(datadir):
        os.makedirs(datadir)

    if not os.path.exists(statesave):
        with open(statesave, 'w+') as f:
            f.write(str(0))

def read_file(filename):
    filetype = filename.split('.')[-1]
    if filetype=='txt':
        filename = os.path.join(datadir, filename)
        with open(filename, 'r') as f:
            return int(f.read())
    elif filetype=='json':
        filename = os.path.join(datadir, filename)
        with open(filename, 'r') as f:
            return json.load(f)
    elif filetype=='yaml':
        with open(filename, 'r') as f:
            return yaml.safe_load(f)

def write_file(filename, val):
    filetype = filename.split('.')[-1]
    filename = os.path.join(datadir, filename)
    if filetype=='str':
        with open(filename, 'w+') as f:
            f.write(str(val))
    else:
        with open(filename, "w+") as f:
            json.dump(val, f, indent=2)

