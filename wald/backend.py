# pylint: disable=no-init,too-few-public-methods
'''Backends for documents.'''

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__base_class__ = declarative_base()


class Node(__base_class__):
    '''A node in the document.'''
    __tablename__ = 'nodes'

    node_id = Column(Integer, primary_key=True)
    name = Column(String)
    content = Column(String)


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
