from orator import Model
from orator.orm import belongs_to

class Token(Model):

    __timestamps__ = False
    __fillable__ = ['pos', 'content']

    @belongs_to
    def sentence(self):
        from .sentence import Sentence
        return Sentence
