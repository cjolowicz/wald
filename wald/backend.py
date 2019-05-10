# pylint: disable=too-few-public-methods
'''Backends for documents.

TODO:

- custom relationships between nodes, e.g. "example for", "member of", "subset of"
- child sequence
'''

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

    def __init__(self, name, *args, **kwargs):
        super(Node, self).__init__(*args, name=name, **kwargs)


class Document(object):
    '''A hierarchically structured document.'''
    def __init__(self, filename=None):
        self._filename = filename or ':memory:'
        self._engine = create_engine('sqlite:///%s' % self._filename, echo=True)
        session_class = sessionmaker(bind=self._engine)
        __base_class__.metadata.create_all(self._engine)
        self._session = session_class()

    @property
    def roots(self):
        '''Return the root nodes of the document.'''
        return self._session.query(Node).filter(
            Node.parent_id.is_(None))

    def add(self, node):
        '''Add the node to the document.'''
        self._session.add(node)

    def remove(self, node):
        '''Remove the node from the document.'''
        self._session.delete(node)

    def save(self):
        '''Save the document.'''
        self._session.commit()

    def insert_document(self, document, parent=None):
        for root in document.roots:
            self.insert_tree(root, parent=parent)

    def insert_tree(self, node, parent=None):
        copy = Node(node.name, content=node.content, parent=parent)
        self.add(copy)
        for child in node.children:
            self.insert_tree(child, parent=copy)

    def save_as(self, filename):
        open(filename, 'w').close() # truncate target
        document = Document(filename)
        document.insert_document(self)
        document.save()
        return document
