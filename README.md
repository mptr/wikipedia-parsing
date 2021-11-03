# Wikipedia parsing

1. Download the xml-Files with `fetch_index.py`
2. Run `parse_wiki.py <filename>.xml`

## Requirements

- PG-Database
- `pip3 install psycopg2-binary orator requests wget spacy`
- `python -m spacy download en_core_web_lg`

## Run the Dev-Database

Start Containers: `docker-compose up -d`

Run Migrations: `orator migrate -c db.py`

## Avtivate venv

create: `python3 -m venv .venv`

avtivate: `source .venv/bin/activate`