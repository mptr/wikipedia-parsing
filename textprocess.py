import re

import spacy
from sql_service import insert_ambiguity

spacy.prefer_gpu()
nlp = spacy.load("en_core_web_lg")

links = re.compile(r'\[\[([^|\[\]]*?)\|?([^|\[\]]*?)\]\]', re.M) # https://regex101.com/r/R5HUKi/2
headline = re.compile(r'^={2,}.*?={2,}\n', re.M)
refs = re.compile(r'<\s*ref[\s\S]*?>[\s\S]*?<\s*\/\s*ref>', re.M) # matches <ref>...</ref>
files = re.compile(r'\[\[File:.*?\]\]', re.M) # [[File:...]]
standaloneNonWord = re.compile(r'')

def textprocess(s):
    s = files.sub("", s) # tidy up text
    s = refs.sub("", s)
    s = headline.sub("", s)

    for i in links.finditer(s): # get links on page and save their texts and linked article in db
        [article, text] = i.groups()
        if(article != ""):
            insert_ambiguity(article, text, 'link')
    s = links.sub(r"\2", s) # remove link target for nlp

    s = "Numerous indigenous peoples occupied Alaska for thousands of years before the arrival of European peoples to the area. Linguistic and DNA studies done here have provided evidence for the settlement of North America by way of the Bering land bridge. At the Upward Sun River site in the Tanana River Valley in Alaska, remains of a six-week-old infant were found. The baby's DNA showed that she belonged to a population that was genetically separate from other native groups present elsewhere in the New World at the end of the Pleistocene. Ben Potter, the University of Alaska Fairbanks archaeologist who unearthed the remains at the Upward Sun River site in 2013, named this new group Ancient Beringians."

    doc = nlp(s)

    # Find named entities, phrases and concepts
    for token in doc:
        print(token.text + " = " + str(token.sentiment))
        # token.ent_type
        #print(entity.text, entity.label_)