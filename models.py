from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import ENUM
import os

# declarative base class
Base = declarative_base()

class Ambiguity(Base):
    __tablename__ = 'ambiguities'
    id = Column(Integer, primary_key=True)
    base = Column(String)
    alt = Column(String)
    kind = Column(ENUM('link', 'redirect', 'spacy', name='ambiguity_kind'))
    page_id = Column(Integer, ForeignKey('pages.id', ondelete="CASCADE"))


class Entity(Base):
    __tablename__ = 'entities'
    id = Column(Integer, primary_key=True)
    start = Column(Integer)
    end = Column(Integer)
    content = Column(String)
    kind = Column(ENUM('CARDINAL','DATE','EVENT','FAC','GPE','LANGUAGE','LAW','LOC','MONEY','NORP','ORDINAL','ORG','PERCENT','PERSON','PRODUCT','QUANTITY','TIME','WORK_OF_ART', name='entity_kind'))
    sentence_id = Column(Integer, ForeignKey('sentences.id', ondelete="CASCADE"))


class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    wikidata_id = Column(String)
    sentences = relationship("Sentence")
    ambiguities = relationship("Ambiguity")


class Sentence(Base):
    __tablename__ = 'sentences'
    id = Column(Integer, primary_key=True)
    pos = Column(Integer)
    entities = relationship("Entity")
    tokens = relationship("Token")
    page_id = Column(Integer, ForeignKey('pages.id', ondelete="CASCADE"))


class Token(Base):
    __tablename__ = 'tokens'
    sentence_id = Column(Integer, ForeignKey('sentences.id', ondelete="CASCADE"))
    pos = Column(Integer)
    content = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint(
            pos,
            sentence_id),
    {})

# use this file as migration runner
if __name__ == '__main__':
    engine = create_engine(os.environ['PSQL_CONNECT_URL'], echo=True)
    Base.metadata.create_all(engine)
