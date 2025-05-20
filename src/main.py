from file_manipulation import initialize, read_file, write_file
from generate_data_new import generate_batch_responses
from ingest_data import ingest
from logging_utils import setup_logging

from datetime import datetime
import logging
import random
import sys

datafile = 'responses.json'
statesave = 'part.txt'
logfile = 'ingest_llm_{}.log'

if __name__ == "__main__":
    setup_logging(logfile)
    initialize(datafile, statesave)

    if len(sys.argv)<2:
        print("run with --stream or --old \neg. `python3 src/main.py --stream`")
        exit()
        
    if sys.argv[1]=='--stream':
        stream=True
    else:
        stream=False

    ingested = 0
    batch = 1000
    no_of_rows = 100_000

    already_ingested = read_file(statesave)

    rem_rows = no_of_rows - already_ingested

    if rem_rows>=batch:
        total_iter = rem_rows//batch
    else:
        total_iter = 1
        batch = rem_rows

    for part in range(total_iter):
        try:
            json_data = generate_batch_responses(batch, stream)
            logging.info(f'Generated {already_ingested+(part*batch)+1} rows')
            write_file(datafile, json_data)
            res = ingest('llm_json', datafile)
            if res:
                ingested += batch
                logging.info(f'Ingested {already_ingested+(part*batch)+1} rows')
                write_file(statesave, ingested)
            else:
                logging.error(f'Exited with {res.status_code}')
                exit()
        except Exception as e:
            write_file(statesave, ingested)
            logging.error(f'Exited with error {e}')
            exit()
    
    write_file(statesave, 0)
