from orator import Model
from orator.orm import belongs_to

class Entity(Model):

    __timestamps__ = False
    __fillable__ = ['start', 'end', 'content', 'kind']

    @belongs_to
    def sentence(self):
        from .sentence import Sentence
        return Sentence
