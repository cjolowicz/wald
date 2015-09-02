# pylint: disable=too-few-public-methods
'''Backends for documents.'''

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

__base_class__ = declarative_base()


class Node(__base_class__):
    '''A node in the document.'''
    __tablename__ = 'nodes'

    node_id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('nodes.node_id'))
    name = Column(String)
    content = Column(String)

    children = relationship(
        'Node',
        cascade='all',
        backref=backref('parent', remote_side='Node.node_id'))

    def __init__(self, name, content='', parent=None):
        self.name = name
        self.content = content
        self.parent = parent
        self.parent_id = parent.node_id if parent else None


class Backend(object):
    '''The backend for a document.'''
    def __init__(self, url=None):
        self._url = url or 'sqlite:///:memory:'
        self._engine = create_engine(self._url, echo=True)
        __base_class__.metadata.create_all(self._engine)

    def create_session(self):
        '''Create a session for managing nodes.'''
        session_class = sessionmaker()
        session_class.configure(bind=self._engine)
        return session_class()
