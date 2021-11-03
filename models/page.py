from orator import Model
import sys, re
from itertools import chain

from orator.orm.utils import has_many

skipUntil = sys.argv[2] if len(sys.argv) > 2 else None

technical_title_regex = re.compile(r'^(?:Wikipedia|Draft|File|Template|Category):\S', re.M)

wikidata_id_regex1 = re.compile(r'{{.*?=(Q\d+).*?}}', re.M)
wikidata_id_regex2 = re.compile(r'wikidata.org[\w/\\]*?(Q\d+)', re.M)

class Page(Model):

    __timestamps__ = False
    __fillable__ = ['title', 'wikidata_id']

    @has_many
    def sentences(self):
        from .sentence import Sentence
        return Sentence

    @has_many
    def ambiguities(self):
        from .ambiguity import Ambiguity
        return Ambiguity

