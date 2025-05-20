import json
import requests
import yaml

af_config = './.airfold/config.yaml'

def read_file(filename):
    filetype = filename.split('.')[-1]
    if filetype=='txt':
        with open(filename, 'r') as f:
            return int(f.read())
    elif filetype=='json':
        with open(filename, 'r') as f:
            return json.load(f)
    elif filetype=='yaml':
        with open(filename, 'r') as f:
            return yaml.safe_load(f)



def ingest(sourcename, datafile):
    auth_code = read_file(af_config)['key']

    data = read_file(datafile)

    response = requests.post('https://api.us.airfold.co/v1/events/{}'.format(sourcename),
                             headers={
                                 'Authorization': 'Bearer {}'.format(auth_code),
                                 'Content-Type': 'application/json', 
                                 'Connection': 'keep-alive'
                                 },
                             json=data
                             )

    if str(response.status_code).startswith('2'):
        return 1
    else:
        return response.status_code

if __name__=="__main__":
    ingest('source_llm_json', 'responses.json')