from orator import Model
from orator.orm.utils import belongs_to, has_many

class Sentence(Model):

    __timestamps__ = False
    __fillable__ = ['pos']

    @has_many
    def entities(self):
        from .entity import Entity
        return Entity

    @has_many
    def tokens(self):
        from .token import Token
        return Token

    @belongs_to
    def page(self):
        from .page import Page
        return Page
