import re, spacy
from sql_service import SqlService

sql = SqlService()

spacy.prefer_gpu()
nlp = spacy.load("en_core_web_lg")

links = re.compile(r'\[\[([^|\[\]]*?)\|?([^|\[\]]*?)\]\]', re.M) # https://regex101.com/r/R5HUKi/2
headline = re.compile(r'^={2,}.*?={2,}\n', re.M)
refs = re.compile(r'<\s*ref[\s\S]*?>[\s\S]*?<\s*\/\s*ref>', re.M) # matches <ref>...</ref>
files = re.compile(r'\[\[File:.*?\]\]\n', re.M) # [[File:...]]\n
stars_and_whitespace = re.compile(r'[\s*]{3,}', re.M)
newlines = re.compile(r'[\n ]+', re.M)
html_comments = re.compile(r'<!--[\s\S]*-->', re.M)
standalone_links = re.compile(r'\n\[\[.*?\]\]', re.M)

def to_sents(s):
    s = s.replace("'''", "") # tidy up text
    s = files.sub("", s) 
    s = standalone_links.sub("", s)
    s = refs.sub("", s)
    s = headline.sub("", s)
    s = stars_and_whitespace.sub("", s)
    s = html_comments.sub("", s)
    s = newlines.sub(" ", s)
    s = s.replace("''", '"')

    for i in links.finditer(s): # get links on page and save their texts and linked article in db
        [article, text] = i.groups()
        if(article != ""):
            sql.insert_ambiguity(article, text, 'link')
    s = links.sub(r"\2", s) # remove link target for nlp

    doc = nlp(s) # Find named entities, phrases and concepts

    return doc.sents
