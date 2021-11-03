import re, sys, spacy
from models.ambiguity import Ambiguity
from models.entity import Entity
from models.token import Token
from util.textprocess import *
from models.page import Page
from models.sentence import Sentence

spacy.prefer_gpu()
nlp = spacy.load("en_core_web_lg")

wikidata_id_regex1 = re.compile(r'{{.*?=(Q\d+).*?}}', re.M)
wikidata_id_regex2 = re.compile(r'wikidata.org[\w/\\]*?(Q\d+)', re.M)

technical_title_regex = re.compile(r'^(?:Wikipedia|Draft|File|Template|Category):\S', re.M)

skipUntil = sys.argv[2] if len(sys.argv) > 2 else None

class Article:
    def __init__(self):
        self.title = ""
        self.text = ""
        self.wikidata_id = ""
        self.ambigs = set()


    def acceptTitle(self, t):
        self.title = self.title + t


    def acceptText(self, t):
        self.text = self.text + t


    def done(self):
        # skip if technical page
        if(technical_title_regex.match(self.title)): return

        # skip while skip arg is set
        global skipUntil
        if(skipUntil):
            if(skipUntil == self.title):
                skipUntil = None
            print("skip %s" % self.title)
            return
        
        self.preprocess()
        self.save()


    def preprocess(self):
        print('processing: %s' % self.title)

        # get wikidata id from captured text
        self.wikidata_id = ','.join(get_wikidata_ids(self.text))
        if self.wikidata_id == "": self.wikidata_id = None
        
        self.text = remove_blocks(self.text)
        self.text = cleanup_text(self.text)

        # links
        self.text, self.ambigs = find_links(self.text)

    def save(self):
        p = Page.create(title=self.title, wikidata_id=self.wikidata_id)
        p.ambiguities().save_many([
            Ambiguity(
                base=a['base'],
                alt=a['alt'],
                kind='link'
            ) for a in self.ambigs
        ])

        doc = nlp(self.text)
        for i,sent in enumerate(doc.sents):
            s = Sentence(pos = i)
            p.sentences().save(s)
            s.entities().save_many([
                Entity(
                    start=e.start,
                    end=e.end,
                    content=e.text,
                    kind=e.label_
                ) for e in sent.ents
            ])
            s.tokens().save_many([
                Token(
                    pos=j,
                    content=t.text
                ) for j,t in enumerate(sent)
            ])


