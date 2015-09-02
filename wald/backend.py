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


class Document(object):
    '''A hierarchically structured document.'''
    def __init__(self, url=None):
        self._url = url or 'sqlite:///:memory:'
        self._engine = create_engine(self._url, echo=True)
        session_class = sessionmaker(bind=self._engine)
        __base_class__.metadata.create_all(self._engine)
        self._session = session_class()

    def roots(self):
        '''Return the root nodes of the document.'''
        return self._session.query(Node).filter(
            Node.parent_id.is_(None))

    def add(self, node):
        '''Add the node to the document.'''
        self._session.add(node)

    def save(self):
        '''Save the document.'''
        self._session.commit()
