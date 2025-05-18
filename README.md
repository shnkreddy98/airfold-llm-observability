# airfold-llm-observability

## Getting Started

- Create an environemnt (Optional)
  `python3 -m venv .venv`
  `source .venv/bin/activate`

- Install all the dependencies
  `python3 install -r requirements.txt`

- Configure airfold
  `af config` and paste your airfold key
  paste the key at .env as well.

- Choose batch and total no of rows to generate
  In `src/main.py` configure batch and no_of_rows as required

- Run the program
  - Use --old flag to generate old date on random, from 2024-01-01 to today. (Recommended config: batch=1000)
  - Use --stream flag to generate streaming data and ingest it. (Recommended config: batch=1000)
