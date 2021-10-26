import psycopg2


class SqlService:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=postgres user=postgres password=changeme host=localhost")

    def __del__(self):
        self.conn.close()

    def insert_ambiguity(self, base, alt, kind):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO ambiguities (base, alt, kind) VALUES (%s, %s, %s) RETURNING "id";', (base.strip(), alt.strip(), kind))
            self.conn.commit()

    def insert_page(self, p):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO pages (title, wikidata_id) VALUES (%s, %s) RETURNING "id";', (p.title, p.wikidata_id))
            pageid = cur.fetchall()[0][0]
            sentcount = entcount = 0
            for s in p.sents:
                sentcount = sentcount+1
                cur.execute('INSERT INTO sentences (text, page_id) VALUES (%s, %s) RETURNING "id";', (s.text, pageid))
                sentid = cur.fetchall()[0][0]
                for e in s.ents:
                    entcount = entcount+1
                    cur.execute('INSERT INTO entities (sentence_id, start, "end", kind) VALUES (%s, %s, %s, %s);', (sentid, e.start_char, e.end_char, e.label_))
            self.conn.commit()
            print('{"title": "%s", "id": %d, "wikidata_id": "%s", "sentcount": %d, "entcount": %d},' % (p.title, pageid, p.wikidata_id, sentcount, entcount))
            


