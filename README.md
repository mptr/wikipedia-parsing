# Wikipedia parsing

1. Download the xml-Files with `fetch_index.py`
2. Run `parse_wiki.py <filename>.xml`

## Requirements

- PG-Database
- `pip install psycopg2-binary sqlalchemy requests wget spacy`
- `python -m spacy download en_core_web_lg`

## Run the Dev-Database

Start Containers: `docker-compose up -d`

Export Connect URL: `export PSQL_CONNECT_URL=postgresql://postgres:changeme@localhost:5432/postgres`

Run Migrations: `python models.py`

___

## Avtivate venv

create: `python -m venv .venv`

avtivate: `source .venv/bin/activate`
