from dotenv import load_dotenv
from file_manipulation import read_file
import requests
import os

load_dotenv()

def ingest(sourcename, datafile):
    auth_code = os.getenv('af_key')

    data = read_file(datafile, filetype='json')

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
