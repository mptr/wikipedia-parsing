from orator import Model
from orator.orm import belongs_to

class Ambiguity(Model):

    __timestamps__ = False
    __fillable__ = ['base', 'alt', 'kind']
    
    @belongs_to
    def page(self):
        from .page import Page
        return Page
    
