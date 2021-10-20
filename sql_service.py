import psycopg2

conn = psycopg2.connect("dbname=wikipedia user=postgres password=changeme host=localhost")

def insert_ambiguity(base, alt, kind):
    cur = conn.cursor()
    print("save %s ambig %s => %s" %(kind, base, alt))
    #cur.execute('INSERT INTO public.ambiguities(base, alt, kind) VALUES (%s, %s, %s);', (base.strip(), alt.strip(), kind))

def insert_sentence():
    pass

def insert_page():
    pass