# Wikipedia parsing

1. Download the xml-Files with `fetch_index.py`
2. Run `parse_wiki.py <filename>.xml`

## Requirements

- PG-Database
- `$ pip3 install psycopg2-binary`

## Dev-Database

```
$ docker-compose up -d
```

## Avtivate venv
```
$ source .env/bin/activate
```