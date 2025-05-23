from file_manipulation import initialize, read_file, write_file
from generate_data import generate_batch_responses
from ingest_data import ingest
from logging_utils import setup_logging

import logging
import sys
import time

datafile = 'responses.json'
statesave = 'part.txt'
logfile = 'ingest_llm_{}.log'

def main(ingested, batch, no_of_rows, stream):
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
                main(ingested, batch, no_of_rows, stream)
        except Exception as e:
            write_file(statesave, ingested)
            logging.error(f'Exited with error {e}')
            main(ingested, batch, no_of_rows, stream)
    
    write_file(statesave, 0)

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
    batch = 2500
    no_of_rows = 5_000_000

    main(ingested, batch, no_of_rows, stream)
